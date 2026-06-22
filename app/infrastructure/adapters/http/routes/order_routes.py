# app/infrastructure/adapters/http/routes/order_routes.py

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.services.order_service import OrderService
from app.infrastructure.adapters.auth.dependencies import get_current_user
from app.infrastructure.adapters.database.config import (
    get_db,  # Tu función de sesión de BD
)
from app.infrastructure.adapters.database.models import UserORM
from app.infrastructure.adapters.database.order_repository_impl import (
    OrderRepositoryImpl,
)
from app.infrastructure.adapters.http.schemas.order_schemas import (
    OrderCreate,
    OrderResponse,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


# Función auxiliar para construir el servicio inyectando sus dependencias
def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    repository = OrderRepositoryImpl(db)
    return OrderService(repository)


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    service: OrderService = Depends(get_order_service),
    current_user: UserORM = Depends(get_current_user),
) -> Any:
    """Endpoint para crear una nueva orden con sus artículos"""
    try:
        # Convertimos el payload de Pydantic a diccionarios nativos para el servicio
        items_dict = [item.model_dump() for item in payload.items]

        # Ejecutamos el caso de uso
        new_order = service.create_order(
            user_id=payload.user_id, gender_str=payload.gender, items_data=items_dict
        )
        return new_order

    except ValueError as e:
        # Si el Dominio o los Value Objects lanzan un ValueError, lo capturamos
        # y lo transformamos en un error 400 Bad Request legible para el cliente
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
    current_user: UserORM = Depends(get_current_user),
) -> Any:
    """Endpoint para consultar una orden por su ID"""
    order = service.get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La orden con ID {order_id} no existe.",
        )
    return order


@router.post("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    service: OrderService = Depends(get_order_service),
    current_user: UserORM = Depends(get_current_user),
) -> Any:
    """Endpoint para cancelación (borrado lógico) de una orden"""
    try:
        success = service.cancel_order(order_id)
        if success:
            return {"message": f"La orden {order_id} ha sido cancelada exitosamente."}

    except ValueError as e:
        # Captura si la orden no existe o si las reglas del dominio impiden cancelarla
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
