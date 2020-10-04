import pytest

from flask_mock_server.server import MockServer


@pytest.fixture
def server():
    return MockServer()


@pytest.fixture
def client(server):
    app = server.app
    yield app.test_client()
