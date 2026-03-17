from __future__ import annotations

import httpx
from fastapi import APIRouter, HTTPException, status
from app.core.config import SUPABASE_URL, SUPABASE_ANON_KEY
from app.deps.auth import get_current_user
from app.schemas.auth import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest):
    url = f"{SUPABASE_URL}/auth/v1/token?grant_type=password"
    headers = {"Content-Type": "application/json", "apikey": SUPABASE_ANON_KEY}
    body = {"email": payload.email, "password": payload.password}
    
    async with httpx.AsyncClient(timeout=20) as client:
        res = await client.post(url, json=body, headers=headers)
        
    if res.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    data = res.json()
    access_token = data["access_token"]
    
    user = get_current_user(authorization=f"Bearer {access_token}")
    
    return LoginResponse(
        access_token=access_token,
        user_id=user["id"],
        role=user["role"],
        full_name=user.get("full_name"),
        cliente_id=user.get("cliente_id"),
    )