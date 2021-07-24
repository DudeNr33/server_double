import requests
import pytest

from server_double.server import MockServer


INFO_URL = "http://localhost:8080/__mock/info"


@pytest.fixture
def new_server():
    server = MockServer()
    yield server
    # make sure the server is stopped if this was not part of the test case
    server.stop()


@pytest.fixture
def started_server(new_server):
    new_server.start()
    yield new_server


def test_start_server(new_server):
    new_server.start()
    assert requests.get(INFO_URL).status_code == 200


def test_start_called_twice_raises_error(started_server):
    """If the server was already started, a RuntimeError must be raised to inform the user
    that the server instance is already running."""
    with pytest.raises(RuntimeError):
        started_server.start()


def test_stop_running_server(started_server):
    started_server.stop()
    with pytest.raises(requests.ConnectionError):
        requests.get(INFO_URL, timeout=1)


def test_stop_already_stopped_server(started_server):
    """It should be possible to call ``stop()`` on an already stopped server without crashing,
    to improve stability/usability if someone accidentally calls this method twice."""
    started_server.stop()
    started_server.stop()


def test_stop_never_started_server(new_server):
    """It should be possible to call ``stop()`` on a server which was not yet started without crashing."""
    new_server.stop()
