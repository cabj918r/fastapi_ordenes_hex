# tests/integration/test_order_api.py
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest

from app.domain.entities.order import Order


@pytest.mark.integration
@patch(
    "app.infrastructure.adapters.database.order_repository_impl.OrderRepositoryImpl.create"
)
def test_create_order_endpoint_with_unittest_mock(mock_create, api_client):
    """Valida el flujo completo de la API aislando la BD con unittest.mock.patch"""

    response_login = api_client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    token = response_login.json()["access_token"]

    # Configuramos el comportamiento del mock nativo
    mock_order = Order(
        id=550,
        user_id=88,
        gender=MagicMock(value="F"),
        status=MagicMock(value="Processing"),
        created_at=datetime.now(timezone.utc),
        items=[],
    )
    mock_create.return_value = mock_order

    payload = {
        "user_id": 88,
        "gender": "F",
        "items": [{"product_id": 12777, "inventory_item_id": 1, "sale_price": 44.99}],
    }

    response = api_client.post(
        "/orders/",
        json=payload,
        headers={"Authorization": "Bearer {token}".format(token=token)},
    )

    # Aseveraciones de la API
    assert response.status_code == 201
    assert response.json()["id"] == 550
    assert response.json()["gender"] == "F"

    # Verificamos que el repositorio realmente fue invocado en la capa de aplicación
    mock_create.assert_called_once()


@pytest.mark.integration
@patch(
    "app.infrastructure.adapters.database.order_repository_impl.OrderRepositoryImpl.get_by_id"
)
def test_get_order_endpoint_with_unittest_mock(mock_get_by_id, api_client):
    """Valida el endpoint de consulta de orden aislando la BD con unittest.mock.patch"""

    response_login = api_client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    token = response_login.json()["access_token"]

    mock_order = Order(
        id=550,
        user_id=88,
        gender=MagicMock(value="F"),
        status=MagicMock(value="Processing"),
        created_at=datetime.now(timezone.utc),
        items=[],
    )
    mock_get_by_id.return_value = mock_order

    response = api_client.get(
        "/orders/550", headers={"Authorization": "Bearer {token}".format(token=token)}
    )

    assert response.status_code == 200
    assert response.json()["id"] == 550
    assert response.json()["gender"] == "F"
    mock_get_by_id.assert_called_once_with(550)


@pytest.mark.integration
@patch(
    "app.infrastructure.adapters.database.order_repository_impl.OrderRepositoryImpl.update"
)
@patch(
    "app.infrastructure.adapters.database.order_repository_impl.OrderRepositoryImpl.get_by_id"
)
def test_cancel_order_endpoint_with_unittest_mock(
    mock_get_by_id, mock_update, api_client
):
    """Valida el endpoint de cancelación de orden aislando la BD con unittest.mock.patch"""

    response_login = api_client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    token = response_login.json()["access_token"]

    mock_order = Order(
        id=550,
        user_id=88,
        gender=MagicMock(value="F"),
        status=MagicMock(value="Processing"),
        created_at=datetime.now(timezone.utc),
        items=[],
    )
    mock_get_by_id.return_value = mock_order

    response = api_client.post(
        "/orders/550/cancel",
        headers={"Authorization": "Bearer {token}".format(token=token)},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "La orden 550 ha sido cancelada exitosamente."
    mock_get_by_id.assert_called_once_with(550)
    mock_update.assert_called_once()
