# app/domain/entities/order.py
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.value_objects.gender import Gender
from app.domain.value_objects.order_status import OrderStatus


@dataclass
class OrderItem:
    product_id: int
    inventory_item_id: int | None
    sale_price: float
    id: int | None = None
    order_id: int | None = None
    user_id: int | None = None
    status: str | None = None
    created_at: datetime | None = None
    shipped_at: datetime | None = None
    delivered_at: datetime | None = None
    returned_at: datetime | None = None


@dataclass
class Order:
    user_id: int
    gender: Gender | None
    items: list[OrderItem]
    id: int | None = None
    status: OrderStatus = field(default_factory=lambda: OrderStatus("Processing"))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    shipped_at: datetime | None = None
    delivered_at: datetime | None = None
    returned_at: datetime | None = None
    num_of_item: int = field(init=False)

    def __post_init__(self) -> None:
        # La entidad calcula el total de ítems basándose en la lista
        self.num_of_item = len(self.items)

    def cancel_order(self) -> None:
        """Regla de negocio: Una orden entregada o ya devuelta no debería poder cancelarse"""
        if self.status.value in {"Complete", "Returned", "Shipped", "Cancelled"}:
            raise ValueError(
                f"No se puede cancelar una orden con estatus '{self.status.value}'."
            )

        self.status = OrderStatus("Cancelled")
