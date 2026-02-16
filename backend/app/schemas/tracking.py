# app/schemas/tracking.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class TrackingCreate(BaseModel):
    despacho_id: int
    lat: float
    lng: float
    fuente: Optional[str] = "manual"