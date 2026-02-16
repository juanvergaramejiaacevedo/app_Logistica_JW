# app/schemas/pedidos.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class PedidoCreate(BaseModel):
    despacho_id: int
    cliente_destino_id: int
    unidades: int
    informacion: Optional[str] = None
    novedad: Optional[str] = None
    solucion: Optional[str] = None
    responsable: Optional[str] = None
    reporte_nocturno: Optional[str] = None
    comentario: Optional[str] = None