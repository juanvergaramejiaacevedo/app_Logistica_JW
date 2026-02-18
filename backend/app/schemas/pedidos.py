# app/schemas/pedidos.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class PedidoCreate(BaseModel):
    despacho_id: int
    cliente_destino_id: int
    unidades: int
    informacion: Optional[str] = None
    estado: Optional[str] = None