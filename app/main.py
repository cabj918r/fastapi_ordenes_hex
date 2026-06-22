# app/main.py
from typing import Any

from fastapi import FastAPI

from app.infrastructure.adapters.http.routes.auth_routes import router as auth_router
from app.infrastructure.adapters.http.routes.order_routes import router as order_router

app = FastAPI(
    title="API de Órdenes",
    version="1.0.0",
    description="API transaccional en capas (Arquitectura Hexagonal + DDD)",
)

app.include_router(auth_router)
# Registramos el router que acabamos de actualizar con el dominio y los servicios
app.include_router(order_router)


@app.get("/")
def health_check() -> dict[str, Any]:
    return {
        "status": "healthy",
        "architecture": "hexagonal",
        "layers": ["domain", "application", "infrastructure"],
    }
