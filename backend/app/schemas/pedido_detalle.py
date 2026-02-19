# app/schemas/pedidos.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Any, Optional

class PedidoDetalleResponse(BaseModel):
    pedido: dict[str, Any]
    despacho: dict[str, Any]
    eventos: list[dict[str, Any]]