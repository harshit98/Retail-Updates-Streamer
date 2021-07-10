import pytest

from producer.app.main import app

from starlette.testclient import TestClient


@pytest.fixture
def test_app():
    client = TestClient(app)
    yield client
