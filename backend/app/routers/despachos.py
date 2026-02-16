# app/routers/despachos.py
from __future__ import annotations

from fastapi import APIRouter, Depends
from app.core.supabase import supabase_user
from app.deps.auth import require_role
from app.schemas.despachos import DespachoCreate

router = APIRouter(prefix="/despachos", tags=["Despachos"])

@router.get("/")
def list_despachos(user=Depends(require_role("admin", "operador"))):
    sb = supabase_user(user["access_token"])
    res = sb.table("despachos").select("*").order("created_at", desc=True).execute()
    return res.data

@router.post("/")
def create_despacho(payload: DespachoCreate, user=Depends(require_role("admin", "operador"))):
    sb = supabase_user(user["access_token"])
    data = payload.model_dump()
    data["created_by"] = user["id"]
    res = sb.table("despachos").insert(data).execute()
    return res.data