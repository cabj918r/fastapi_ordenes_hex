# app/domain/repositories/order_repository.py
from abc import ABC, abstractmethod
from typing import Optional

from app.domain.entities.order import Order


class OrderRepository(ABC):
    """
    PUERTO (Interface): Define el contrato que cualquier adaptador
    de base de datos debe cumplir. Pertenece al Dominio.
    """

    @abstractmethod
    def get_by_id(self, order_id: int) -> Optional[Order]:
        """Recupera una orden por su ID"""
        pass

    @abstractmethod
    def create(self, order: Order) -> Order:
        """Guarda una orden completa con sus detalles en la base de datos"""
        pass

    @abstractmethod
    def update(self, order: Order) -> Order:
        """Actualiza el estado o datos de una orden existente"""
        pass
