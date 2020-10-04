import pytest

from flask_mock_server.server import MockServer


def test_port():
    server = MockServer(
        config={
            "port": 8083
        }
    )
    assert server.port == 8083


@pytest.mark.parametrize(
    "endpoint_config",
    [
        {"/endpoint": {"status_code": 200}},
        {"/endpoint": {"status_code": 204}},
        {"/endpoint": {"status_code": 303}},
    ]
)
def test_single_endpoint_get(endpoint_config):
    server = MockServer(
        config={
            "endpoints": endpoint_config
        }
    )
    server.app.config["TESTING"] = True
    test_client = server.app.test_client()
    expected_status = endpoint_config["/endpoint"].get("status_code", 200)
    expected_content = endpoint_config["/endpoint"].get("content", b"")

    response = test_client.get(server.url + "/endpoint")

    assert response.status_code == expected_status
    assert response.data == expected_content
