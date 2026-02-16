# 🚚 App Logística JW -- Backend API

Backend del sistema de gestión logística desarrollado con **FastAPI +
Supabase**, diseñado para integrarse con una aplicación móvil/web
construida en **FlutterFlow**.

Permite gestionar:

-   🔐 Autenticación con Supabase
-   👥 Control de roles (`admin`, `operador`, `cliente`)
-   🚛 Despachos
-   📦 Pedidos
-   📝 Eventos por pedido
-   📍 Tracking de despacho
-   🔒 Seguridad con RLS (Row Level Security)

------------------------------------------------------------------------

# 🏗️ Arquitectura

FlutterFlow (Frontend)\
↓\
FastAPI (Backend)\
↓\
Supabase (PostgreSQL + Auth + RLS)

-   La autenticación se realiza con **Supabase Auth**
-   FastAPI valida el JWT
-   Todas las consultas se ejecutan respetando **RLS**
-   Los clientes solo ven sus propios pedidos y tracking

------------------------------------------------------------------------

# 📁 Estructura del Proyecto

    backend/
    │
    ├── app/
    │   ├── core/
    │   │   ├── config.py
    │   │   └── supabase.py
    │   │
    │   ├── deps/
    │   │   └── auth.py
    │   │
    │   ├── routers/
    │   │   ├── me.py
    │   │   ├── despachos.py
    │   │   ├── pedidos.py
    │   │   ├── eventos.py
    │   │   └── tracking.py
    │   │
    │   ├── schemas/
    │   │   ├── despachos.py
    │   │   ├── pedidos.py
    │   │   ├── eventos.py
    │   │   └── tracking.py
    │   │
    │   └── main.py
    │
    ├── .env.example
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

# 🔐 Roles del Sistema

  Rol          Permisos principales
  ------------ ---------------------------------------------------------
  `admin`      Acceso total
  `operador`   Crear y gestionar despachos, pedidos, eventos
  `cliente`    Ver únicamente sus pedidos, eventos visibles y tracking

El control se implementa mediante:

-   `profiles.role`
-   `cliente_usuarios`
-   Policies RLS en Supabase
-   `require_role()` en FastAPI

------------------------------------------------------------------------

# 🛠️ Instalación Local

## 1️⃣ Clonar repositorio

``` bash
git clone https://github.com/TU_USUARIO/app_Logistica_JW.git
cd app_Logistica_JW/backend
```

## 2️⃣ Crear entorno virtual

``` bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Mac/Linux
```

## 3️⃣ Instalar dependencias

``` bash
pip install -r requirements.txt
```

## 4️⃣ Configurar variables de entorno

Copia `.env.example` y crea tu `.env`:

``` bash
copy .env.example .env
```

Editar `.env`:

``` env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=xxxxx
SUPABASE_SERVICE_ROLE_KEY=xxxxx
```

⚠️ Nunca subir `.env` a GitHub.

## 5️⃣ Ejecutar servidor

``` bash
uvicorn app.main:app --reload
```

Servidor disponible en:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# 🔑 Autenticación

El frontend (FlutterFlow) debe:

1.  Autenticarse con Supabase (email/password)
2.  Obtener el `access_token`
3.  Enviar en cada request:

Authorization: Bearer `<access_token>`{=html}

------------------------------------------------------------------------

# 📡 Endpoints Principales

## Auth

GET /me

## Despachos

GET /despachos/\
POST /despachos/

## Pedidos

GET /pedidos/\
GET /pedidos/mis\
POST /pedidos/

## Eventos

GET /eventos/?pedido_id=\
POST /eventos/

## Tracking

GET /tracking/?despacho_id=\
POST /tracking/

------------------------------------------------------------------------

# 🔒 Seguridad

-   JWT validado en cada request
-   Supabase RLS habilitado en todas las tablas
-   Cliente solo accede a sus datos
-   Admin/Operador gestionan operaciones

------------------------------------------------------------------------

# 🚀 Deployment

Recomendado:

-   Render
-   Railway
-   Fly.io
-   VPS con Docker

Ejemplo con Render:

Build Command: pip install -r requirements.txt

Start Command: uvicorn app.main:app --host 0.0.0.0 --port 10000

------------------------------------------------------------------------

# 📊 Base de Datos

Gestionada en Supabase con:

-   RLS habilitado
-   Función `current_role()`
-   Policies para:
    -   admin/operador
    -   cliente (acceso restringido)

------------------------------------------------------------------------

# 📌 Roadmap Futuro

-   📸 Subida de imágenes en eventos
-   🗺️ Tracking en tiempo real (mapa)
-   📊 Dashboard con métricas
-   🔔 Notificaciones push
-   📦 Estado automático de pedidos

------------------------------------------------------------------------

# 👨‍💻 Autor

Desarrollado por **Daniel Vergara**\
Proyecto: App Logística JW\
Stack: FastAPI + Supabase + FlutterFlow
