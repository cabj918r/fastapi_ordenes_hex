# app/infrastructure/adapters/http/schemas/order_schemas.py
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

# ==========================================
# 1. Esquemas para los ARTÍCULOS (Items)
# ==========================================


class OrderItemCreate(BaseModel):
    product_id: int
    inventory_item_id: int
    sale_price: float


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    product_id: int
    sale_price: float
    inventory_item_id: int | None = None
    user_id: int | None = None
    status: str | None = None
    created_at: datetime | None = None
    shipped_at: datetime | None = None
    delivered_at: datetime | None = None
    returned_at: datetime | None = None


# ==========================================
# 2. Esquemas para la ORDEN PRINCIPAL
# ==========================================


class OrderCreate(BaseModel):
    user_id: int
    gender: str = Field(..., description="Género: 'M' o 'F'")
    items: list[OrderItemCreate]


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    gender: str
    status: str
    num_of_item: int
    total_amount: float | None = None
    created_at: datetime

    # Las fechas de ciclo de vida son opcionales al crear una orden
    shipped_at: datetime | None = None
    delivered_at: datetime | None = None
    returned_at: datetime | None = None

    items: list[OrderItemResponse]

    @field_validator("gender", "status", mode="before")
    @classmethod
    def transform_value_objects(cls, v: Any) -> str:
        if hasattr(v, "value"):
            return str(v.value)
        return str(v)
