# app/core/supabase.py
from __future__ import annotations

from supabase import create_client, Client
from app.core.config import SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY

# Cliente admin: BYPASS RLS (úsalo solo en auth/validaciones y operaciones internas)
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def supabase_user(access_token: str) -> Client:
    """
    Crea un cliente que actúa COMO el usuario autenticado, respetando RLS.
    """
    client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    client.postgrest.auth(access_token)
    return client