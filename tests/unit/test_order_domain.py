# tests/unit/test_order_domain.py
from datetime import datetime, timezone

import pytest
from hypothesis import given
from hypothesis import strategies as st

from app.domain.entities.order import Order, OrderItem
from app.domain.value_objects.gender import Gender
from app.domain.value_objects.order_status import OrderStatus


# -------------------------------------------------------------------------
# PARAMETRIZACIÓN: Probamos múltiples estados inválidos en una sola función
# -------------------------------------------------------------------------
@pytest.mark.parametrize("invalid_status", ["Complete", "Returned", "Shipped"])
@pytest.mark.unit
def test_cancel_order_in_invalid_states_raises_error(invalid_status):
    """Garantiza que una orden no pueda cancelarse si ya pasó de la etapa de procesamiento"""
    order = Order(
        id=1,
        user_id=100,
        gender=Gender("F"),
        status=OrderStatus(invalid_status),
        created_at=datetime.now(timezone.utc),
        items=[],
    )

    with pytest.raises(ValueError, match="No se puede cancelar una orden con estatus"):
        order.cancel_order()


# -------------------------------------------------------------------------
# PROPERTY-BASED TESTING: Hypothesis genera ids y totales de forma masiva
# -------------------------------------------------------------------------
@given(
    user_id=st.integers(min_value=1, max_value=100000),
    price=st.floats(min_value=0.01, max_value=5000.00),
)
@pytest.mark.unit
def test_order_totals_and_attributes_with_hypothesis(user_id, price):
    """Prueba basada en propiedades: No importa el ID o precio generado, el conteo debe ser consistente"""
    items = [
        OrderItem(
            id=1, order_id=9, product_id=202, inventory_item_id=10, sale_price=price
        )
    ]

    order = Order(
        id=9,
        user_id=user_id,
        gender=Gender("M"),
        status=OrderStatus("Processing"),
        created_at=datetime.now(timezone.utc),
        items=items,
    )

    assert order.num_of_item == 1
    assert order.user_id == user_id
    assert order.items[0].sale_price == price
