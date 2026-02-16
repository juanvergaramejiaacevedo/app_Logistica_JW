# app/schemas/eventos.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class EventoCreate(BaseModel):
    pedido_id: int
    tipo: str
    descripcion: str
    visible_cliente: bool = False
    foto_path: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None