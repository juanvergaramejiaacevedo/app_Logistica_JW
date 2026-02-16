# app/schemas/despachos.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class DespachoCreate(BaseModel):
    cliente_origen_id: int
    placa: Optional[str] = None
    conductor_nombre: Optional[str] = None