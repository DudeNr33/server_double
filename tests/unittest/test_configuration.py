"""
Unittests checking the initialization of the ``MockServer`` class and evaluation of the config passed to it.
"""
from unittest.mock import patch

import pytest

from server_double.server import Endpoint, MockServer


def test_port():
    server = MockServer(config={"port": 8083})
    assert server.port == 8083


@pytest.mark.parametrize(
    "url,config",
    [
        ("/endpoint", {"status_code": 200}),
        ("/resource", {"status_code": 204}),
        ("/foobar", {"status_code": 303}),
    ],
)
def test_single_endpoint(url, config):
    with patch("server_double.server.cherrypy") as cherrypy_mock:
        _ = MockServer(config={"endpoints": {url: config}})
    root, script_path = cherrypy_mock.tree.mount.call_args[0]
    assert script_path == url
    assert isinstance(root, Endpoint)
    assert root.url == url
    assert root.default_status == config["status_code"]
