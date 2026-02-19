# app/routers/pedidos.py
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, HTTPException
from app.core.supabase import supabase_user
from app.deps.auth import require_role
from app.schemas.pedidos import PedidoCreate
from app.schemas.pedido_detalle import PedidoDetalleResponse

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
        "ultimos_eventos": eventos_res.data or [], # nombre consistente
    }