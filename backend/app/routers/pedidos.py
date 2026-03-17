# app/routers/pedidos.py
from __future__ import annotations

import os
import datetime
from fastapi import APIRouter, Depends, Query, HTTPException, UploadFile, File
from core.supabase import supabase_user, supabase_admin
from deps.auth import require_role
from schemas.pedidos import PedidoCreate
from schemas.pedido_detalle import PedidoDetalleResponse
from schemas.documentos import PedidoDocumentoOut

BUCKET = "pedido_docs"

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.get("/")
def list_pedidos(
    despacho_id: int | None = Query(default=None),
    user=Depends(require_role("admin", "operador")),
):
    sb = supabase_user(user["access_token"])
    q = sb.table("pedidos").select("*").order("created_at", desc=True)
    if despacho_id is not None:
        q = q.eq("despacho_id", despacho_id)
    return q.execute().data

@router.post("/")
def create_pedido(payload: PedidoCreate, user=Depends(require_role("admin", "operador"))):
    sb = supabase_user(user["access_token"])
    return sb.table("pedidos").insert(payload.model_dump()).execute().data

@router.get("/mis")
def mis_pedidos(user=Depends(require_role("cliente"))):
    sb = supabase_user(user["access_token"])
    cliente_id = user["cliente_id"]

    # Incluye despacho embebido (para el detalle en FlutterFlow)
    return (
        sb.table("pedidos")
        .select("*, despachos(id, fecha_salida, cliente_origen_id, placa, conductor_nombre, estado)")
        .eq("cliente_destino_id", cliente_id)
        .order("created_at", desc=True)
        .execute()
        .data
    )
    
@router.get("/{pedido_id}/detalle", response_model=PedidoDetalleResponse)
def pedido_detalle(pedido_id: int, user=Depends(require_role("admin", "operador", "cliente"))):
    sb = supabase_user(user["access_token"])

    pedido_res = sb.table("pedidos").select("*").eq("id", pedido_id).single().execute()
    if not pedido_res.data:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    pedido_data = pedido_res.data

    despacho_data = None
    if pedido_data.get("despacho_id") is not None:
        despacho_res = (
            sb.table("despachos")
            .select("id, cliente_origen_id, placa, conductor_nombre, estado, created_at")
            .eq("id", pedido_data["despacho_id"])
            .single()
            .execute()
        )
        despacho_data = despacho_res.data

    eventos_q = (
        sb.table("eventos_pedido")
        .select("id, tipo, descripcion, visible_cliente, created_at")
        .eq("pedido_id", pedido_id)
        .order("created_at", desc=True)
        .limit(3)
    )
    if user.get("role") == "cliente":
        eventos_q = eventos_q.eq("visible_cliente", True)

    eventos_res = eventos_q.execute()

    return {
        "pedido": pedido_data,
        "despacho": despacho_data,                 # puede ser None
        "eventos": eventos_res.data or [], # nombre consistente
    }
    
@router.post("/{pedido_id}/documentos/upload")
def upload_documentos_pedido(
    pedido_id: int,
    files: list[UploadFile] = File(...),
    user=Depends(require_role("admin", "operador")),
):
    sb = supabase_user(user["access_token"])

    # 1) Traer pedido para saber despacho_id y validar que exista
    pres = sb.table("pedidos").select("id, despacho_id").eq("id", pedido_id).execute()
    if not pres.data:
        raise HTTPException(404, "Pedido no encontrado")
    pedido = pres.data[0]
    despacho_id = pedido.get("despacho_id")

    saved = []
    for f in files:
        ext = os.path.splitext(f.filename)[1].lower()
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        safe_name = f.filename.replace(" ", "_")
        path = f"despachos/{despacho_id}/pedidos/{pedido_id}/{ts}_{safe_name}"

        content = f.read()

        # 2) Subir a Storage (privado)
        up = supabase_admin.storage.from_(BUCKET).upload(
            path,
            content,
            {"content-type": f.content_type or "application/octet-stream", "upsert": "true"},
        )

        # 3) Registrar en tabla pedido_documentos
        ins = (
            sb.table("pedido_documentos")
            .insert({
                "pedido_id": pedido_id,
                "despacho_id": despacho_id,
                "bucket": BUCKET,
                "file_path": path,
                "file_name": f.filename,
                "content_type": f.content_type,
                "size_bytes": len(content),
                "uploaded_by": user["id"],
            })
            .execute()
        )
        saved.append(ins.data[0])

    return {"ok": True, "count": len(saved), "items": saved}


@router.get("/{pedido_id}/documentos", response_model=list[PedidoDocumentoOut])
def list_documentos_pedido(
    pedido_id: int,
    user=Depends(require_role("admin", "operador", "cliente")),
):
    sb = supabase_user(user["access_token"])

    # RLS se encarga de filtrar si es cliente
    res = (
        sb.table("pedido_documentos")
        .select("id,pedido_id,despacho_id,file_name,file_path,content_type,created_at")
        .eq("pedido_id", pedido_id)
        .order("created_at", desc=True)
        .execute()
    )
    items = res.data or []

    # generar signed_url por cada documento
    out = []
    for it in items:
        signed = supabase_admin.storage.from_(BUCKET).create_signed_url(it["file_path"], 3600)
        it["signed_url"] = signed.get("signedURL") if isinstance(signed, dict) else getattr(signed, "signedURL", None)
        out.append(it)

    return out