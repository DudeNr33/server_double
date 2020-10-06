import time

import pytest
import requests

from server_double.server import MockServer


@pytest.fixture(scope="module")
def mock_server():
    server = MockServer()
    server.start()
    time.sleep(2)
    yield server
    server.shutdown_server()


def test_json_response(mock_server):
    uri = "/json"
    expected_response = ["hello", "world"]
    mock_server.add_json_response(
        url=uri,
        serializable=expected_response
    )

    actual_response = requests.get(mock_server.url + uri).json()

    assert actual_response == expected_response
