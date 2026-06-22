from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.adapters.database.config import Base


class ProductORM(Base):
    """Mapea la tabla de productos reflejando el esquema real de theLook eCommerce"""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cost: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # Costo de fabricación/compra
    category: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    brand: Mapped[str | None] = mapped_column(String, index=True, nullable=True)
    retail_price: Mapped[float] = mapped_column(
        Float, nullable=False
    )  # Precio de venta al público
    department: Mapped[str | None] = mapped_column(
        String, nullable=True
    )  # Men, Women, etc.
    sku: Mapped[str | None] = mapped_column(
        String, unique=True, index=True, nullable=True
    )
    distribution_center_id: Mapped[int | None] = mapped_column(Integer, nullable=True)


class OrderORM(Base):
    """Mapea la tabla principal de Órdenes (Cabecera) igual al dataset analítico"""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String, default="Processing", nullable=False)
    gender: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    returned_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    shipped_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    num_of_item: Mapped[int] = mapped_column(
        Integer, default=1, nullable=False
    )  # Cantidad total de artículos en la orden

    # Relación uno-a-muchos con las líneas de detalle
    items: Mapped[list["OrderItemORM"]] = relationship(
        "OrderItemORM", back_populates="order", cascade="all, delete-orphan"
    )


class OrderItemORM(Base):
    """Mapea la tabla de detalles de la Orden (Líneas de compra individuales)"""

    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("products.id"), nullable=False
    )
    inventory_item_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String, default="Processing", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    shipped_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    sale_price: Mapped[float] = mapped_column(
        Float, nullable=False
    )  # El precio real al que se cobró el artículo

    # Relaciones para navegar entre objetos en Python
    order: Mapped["OrderORM"] = relationship("OrderORM", back_populates="items")
    product: Mapped["ProductORM"] = relationship("ProductORM")


class UserORM(Base):
    __tablename__ = "api_users"

    username: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
