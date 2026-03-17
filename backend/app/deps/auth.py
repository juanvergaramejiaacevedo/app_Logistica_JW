# app/deps/auth.py
from __future__ import annotations

from typing import Optional, Dict, Any
from fastapi import Header, HTTPException, status

from app.core.supabase import supabase_admin


def _extract_token(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Falta Authorization")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization inválido (usa Bearer)")
    return parts[1]


def get_current_user(authorization: Optional[str] = Header(default=None)) -> Dict[str, Any]:
    token = _extract_token(authorization)

    # 1) Validar JWT y obtener user_id desde Supabase Auth
    auth_user = supabase_admin.auth.get_user(token)
    if not auth_user or not getattr(auth_user, "user", None):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user_id = auth_user.user.id  # uuid

    # 2) Obtener rol desde profiles
    prof = (
        supabase_admin.table("profiles")
        .select("id, role, full_name")
        .eq("id", user_id)
        .single()
        .execute()
    )
    if not prof.data:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Perfil no encontrado en profiles")

    role = prof.data.get("role")
    full_name = prof.data.get("full_name")

    user: Dict[str, Any] = {
        "id": user_id,
        "role": role,
        "full_name": full_name,
        "access_token": token,  # CLAVE: para supabase_user()
    }

    # 3) Si es cliente, amarrar cliente_id
    if role == "cliente":
        rel = (
            supabase_admin.table("cliente_usuarios")
            .select("cliente_id, activo")
            .eq("user_id", user_id)
            .eq("activo", True)
            .single()
            .execute()
        )
        if not rel.data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El usuario cliente no tiene relación activa con cliente_usuarios",
            )
        user["cliente_id"] = rel.data["cliente_id"]

    return user


def require_role(*roles: str):
    """
    Dependency factory: requiere que el usuario tenga alguno de los roles permitidos.
    Uso: user = Depends(require_role("admin","operador"))
    """
    def _dep(authorization: Optional[str] = Header(default=None)) -> Dict[str, Any]:
        user = get_current_user(authorization)
        if user.get("role") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No autorizado para este recurso")
        return user

    return _dep