# app/schemas/documentos.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class PedidoDocumentoOut(BaseModel):
    id: int
    pedido_id: int
    despacho_id: Optional[int] = None
    file_name: str
    file_path: str
    content_type: Optional[str] = None
    created_at: str
    signed_url: Optional[str] = None