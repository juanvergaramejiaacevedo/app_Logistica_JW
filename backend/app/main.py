# app/main.py
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import me, auth, despachos, pedidos, eventos, tracking

app = FastAPI(title="Logística JW MVP - API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod pon tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(me.router)
app.include_router(despachos.router)
app.include_router(pedidos.router)
app.include_router(eventos.router)
app.include_router(tracking.router)