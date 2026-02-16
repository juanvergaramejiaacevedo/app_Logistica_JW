# app/routers/eventos.py
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from app.core.supabase import supabase_user
from app.deps.auth import require_role
from app.schemas.eventos import EventoCreate

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.get("/")
def list_eventos(
    pedido_id: int = Query(...),
    user=Depends(require_role("admin", "operador", "cliente")),
):
    sb = supabase_user(user["access_token"])
    q = (
        sb.table("eventos_pedido")
        .select("*")
        .eq("pedido_id", pedido_id)
        .order("created_at", desc=True)
    )

    # Si es cliente, solo eventos visibles
    if user.get("role") == "cliente":
        q = q.eq("visible_cliente", True)

    return q.execute().data

@router.post("/")
def create_evento(payload: EventoCreate, user=Depends(require_role("admin", "operador"))):
    sb = supabase_user(user["access_token"])
    data = payload.model_dump()
    data["responsable_id"] = user["id"]
    return sb.table("eventos_pedido").insert(data).execute().data