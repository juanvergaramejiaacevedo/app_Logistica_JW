# app/routers/me.py
from __future__ import annotations

from fastapi import APIRouter, Depends
from app.deps.auth import get_current_user

router = APIRouter(prefix="/me", tags=["Auth"])

@router.get("")
def me(user=Depends(get_current_user)):
    # Devuelve info mínima
    return {
        "id": user["id"],
        "role": user["role"],
        "full_name": user.get("full_name"),
        "cliente_id": user.get("cliente_id"),
    }