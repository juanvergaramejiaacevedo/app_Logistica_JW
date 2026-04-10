# app/routers/clientes.py
from __future__ import annotations

from fastapi import APIRouter, Depends, Query, HTTPException
from app.core.supabase import supabase_user
from app.deps.auth import require_role
from app.schemas.clientes import ClienteCreate, ClienteOut

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=list[ClienteOut])
def list_clientes(user=Depends(require_role("admin", "operador"))):
    
    sb = supabase_user(user["access_token"])
    
    res = sb.table("clientes").select("*").order("created_at", desc=True).execute()
    
    return res.data or []

@router.post("/", response_model=ClienteOut)
def create_cliente(payload: ClienteCreate, user=Depends(require_role("admin", "operador"))):
    
    sb = supabase_user(user["access_token"])
    
    data = payload.model_dump()
    
    #data["created_by"] = user["id"]
    
    res = sb.table("clientes").insert(data).execute()
    
    #if res.error:
        #raise HTTPException(status_code=400, detail=res.error.message)
   
    if not res.data:
        raise HTTPException(status_code=400, detail="Error al crear cliente")
    
    return res.data[0]