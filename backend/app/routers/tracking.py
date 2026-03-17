# app/routers/tracking.py
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from app.core.supabase import supabase_user
from app.deps.auth import require_role
from app.schemas.tracking import TrackingCreate

router = APIRouter(prefix="/tracking", tags=["Tracking"])

@router.get("/")
def list_tracking(
    despacho_id: int = Query(...),
    user=Depends(require_role("admin", "operador", "cliente")),
):
    sb = supabase_user(user["access_token"])
    return (
        sb.table("tracking_despacho")
        .select("*")
        .eq("despacho_id", despacho_id)
        .order("created_at", desc=True)
        .execute()
        .data
    )

@router.post("/")
def add_tracking(payload: TrackingCreate, user=Depends(require_role("admin", "operador"))):
    sb = supabase_user(user["access_token"])
    return sb.table("tracking_despacho").insert(payload.model_dump()).execute().data