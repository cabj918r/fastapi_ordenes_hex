"""Test para diagnóstico del endpoint /auth/login"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.integration
def test_login_with_admin_credentials():
    """Prueba login con credenciales admin de la BD"""
    response = client.post(
        "/auth/login", json={"username": "admin", "password": "admin123"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.integration
def test_login_with_usuario_credentials():
    """Prueba login con credenciales usuario de la BD"""
    response = client.post(
        "/auth/login", json={"username": "usuario", "password": "usuario123"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.integration
def test_login_with_invalid_password():
    """Prueba login con contraseña incorrecta"""
    response = client.post(
        "/auth/login", json={"username": "admin", "password": "wrongpassword"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Usuario o contraseña incorrectos"


@pytest.mark.integration
def test_login_with_nonexistent_user():
    """Prueba login con usuario que no existe"""
    response = client.post(
        "/auth/login", json={"username": "noexiste", "password": "anypassword"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 401
    assert response.json()["detail"] == "Usuario o contraseña incorrectos"
