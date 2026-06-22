# app/application/services/order_service.py
from typing import Any

from app.domain.entities.order import Order, OrderItem
from app.domain.repositories.order_repository import OrderRepository
from app.domain.value_objects.gender import Gender


class OrderService:
    """
    Capa de Aplicación: Orquesta los Casos de Uso del negocio.
    Solo depende de las abstracciones del Dominio (Puertos), nunca de la BD real.
    """

    def __init__(self, order_repository: OrderRepository):
        # Inyección de dependencias: Recibimos el puerto abstracto
        self.order_repository = order_repository

    def create_order(
        self, user_id: int, gender_str: str, items_data: list[dict[str, Any]]
    ) -> Order:
        """Caso de Uso: Crear y procesar una nueva orden"""

        # 1. Transformamos los tipos primitivos a los Value Objects del Dominio
        domain_gender = Gender(gender_str)

        # 2. Construimos la lista de Entidades de detalle (OrderItem)
        domain_items = [
            OrderItem(
                product_id=item["product_id"],
                inventory_item_id=item["inventory_item_id"],
                sale_price=float(item["sale_price"]),
            )
            for item in items_data
        ]

        # 3. Instanciamos la Entidad Raíz (Order)
        domain_order = Order(user_id=user_id, gender=domain_gender, items=domain_items)

        # 4. Persistimos usando el puerto abstracto. El adaptador se encargará del SQL.
        return self.order_repository.create(domain_order)

    def get_order(self, order_id: int) -> Order | None:
        """Caso de Uso: Consultar una orden existente por su ID"""
        return self.order_repository.get_by_id(order_id)

    def cancel_order(self, order_id: int) -> bool:
        """Caso de Uso: Cancelar una orden (Borrado lógico)"""
        # 1. Primero buscamos la orden para verificar si existe
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise ValueError(f"No se encontró la orden con ID {order_id}")

        # 2. Le pedimos a la entidad de dominio que intente cancelarse (aplica reglas de negocio)
        order.cancel_order()

        # 3. Si el dominio da luz verde, mandamos a actualizar el estado en la persistencia
        self.order_repository.update(order)

        return True
