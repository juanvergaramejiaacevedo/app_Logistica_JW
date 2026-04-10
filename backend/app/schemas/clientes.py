# app/schemas/clientes.py
from __future__ import annotations

from pydantic import BaseModel, EmailStr
from typing import Optional

class ClienteCreate(BaseModel):
    nombre: str
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    
class ClienteOut(BaseModel):
    id: int
    nombre: str
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    created_at: str