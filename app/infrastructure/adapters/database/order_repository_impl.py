# app/infrastructure/adapters/database/order_repository_impl.py
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.order import Order, OrderItem
from app.domain.repositories.order_repository import OrderRepository
from app.domain.value_objects.gender import Gender
from app.domain.value_objects.order_status import OrderStatus
from app.infrastructure.adapters.database.models import (
    OrderItemORM,
    OrderORM,
)


class OrderRepositoryImpl(OrderRepository):
    """
    ADAPTADOR de Persistencia: Implementación real del puerto del dominio.
    Traduce el lenguaje del dominio al lenguaje de la base de datos (SQLAlchemy 2.0).
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_id(self, order_id: int) -> Order | None:
        """Busca en la BD usando la nueva sintaxis de ejecución y reconstruye la Entidad"""
        # SQLAlchemy 2.0 prefiere session.scalar(select(...)) sobre session.query(...)
        stmt = select(OrderORM).where(OrderORM.id == order_id)
        order_orm = self.db.scalar(stmt)

        if not order_orm:
            return None

        # 1. Traducimos los ítems ORM a ítems de Dominio de forma directa (ya están tipados)
        domain_items = [
            OrderItem(
                id=item.id,
                order_id=item.order_id,
                product_id=item.product_id,
                inventory_item_id=item.inventory_item_id,
                sale_price=item.sale_price,
                user_id=item.user_id,
                status=item.status,
                created_at=item.created_at,
                shipped_at=item.shipped_at,
                delivered_at=item.delivered_at,
                returned_at=item.returned_at,
            )
            for item in order_orm.items
        ]

        # 2. Reconstruimos la Entidad Raíz (Order) de forma limpia
        return Order(
            id=order_orm.id,
            user_id=order_orm.user_id,
            gender=Gender(order_orm.gender) if order_orm.gender else None,
            status=OrderStatus(order_orm.status),
            created_at=order_orm.created_at,
            shipped_at=order_orm.shipped_at,
            delivered_at=order_orm.delivered_at,
            returned_at=order_orm.returned_at,
            items=domain_items,
        )

    def create(self, order: Order) -> Order:
        """Traduce la Entidad de Dominio a Modelos ORM y los guarda"""

        # 1. Creamos el registro de la orden principal
        order_orm = OrderORM(
            user_id=order.user_id,
            gender=order.gender.value if order.gender else None,
            status=order.status.value,
            num_of_item=order.num_of_item,
            created_at=order.created_at,
        )

        self.db.add(order_orm)
        self.db.flush()  # Genera el ID de la orden de manera segura

        # 2. Creamos los registros de los detalles (OrderItemORM)
        for item in order.items:
            item_orm = OrderItemORM(
                user_id=order.user_id,
                status=order.status.value,
                product_id=item.product_id,
                inventory_item_id=item.inventory_item_id,
                sale_price=item.sale_price,
                created_at=order.created_at,
                shipped_at=order.shipped_at,
                delivered_at=order.delivered_at,
                returned_at=order.returned_at,
            )
            order_orm.items.append(item_orm)

        self.db.commit()
        self.db.refresh(order_orm)

        # 3. Retornamos la entidad de dominio actualizada
        order.id = order_orm.id
        for i, item_orm in enumerate(order_orm.items):
            order.items[i].id = item_orm.id
            order.items[i].order_id = order_orm.id
            order.items[i].user_id = item_orm.user_id
            order.items[i].status = item_orm.status
            order.items[i].created_at = item_orm.created_at

        return order

    def update(self, order: Order) -> Order:
        """Actualiza los datos de una orden existente"""
        # Sintaxis moderna para buscar el registro
        stmt = select(OrderORM).where(OrderORM.id == order.id)
        order_orm = self.db.scalar(stmt)

        if not order_orm:
            raise ValueError(
                f"No se encontró la orden con ID {order.id} para actualizar."
            )

        # 2. Sincronizamos los cambios directamente sin type: ignores
        # Gracias a Mapped[str], el linter sabe que aceptar un string es perfectamente válido
        order_orm.status = order.status.value
        order_orm.gender = order.gender.value if order.gender else None
        order_orm.num_of_item = order.num_of_item
        order_orm.shipped_at = order.shipped_at
        order_orm.delivered_at = order.delivered_at
        order_orm.returned_at = order.returned_at

        # 3. Actualizamos los campos espejo en order_items que pide theLook
        for item in order_orm.items:
            item.status = order.status.value
            item.shipped_at = order.shipped_at
            item.delivered_at = order.delivered_at
            item.returned_at = order.returned_at

        # 4. Confirmamos los cambios de toda la unidad de trabajo
        self.db.commit()
        return order
