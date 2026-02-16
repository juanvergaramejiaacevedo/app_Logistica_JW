# app/routers/pedidos.py
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from app.core.supabase import supabase_user
from app.deps.auth import require_role
from app.schemas.pedidos import PedidoCreate

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