# tests/conftest.py
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def api_client():
    """Fixture que provee el cliente HTTP de FastAPI para pruebas E2E/Integración"""
    return TestClient(app)


@pytest.fixture
def mock_repo():
    """Fixture que genera un mock puro del repositorio utilizando unittest.mock"""
    repo = MagicMock()
    return repo
