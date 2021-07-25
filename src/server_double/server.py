"""
Logic for creating and managing the mock server.
"""

from enum import Enum

import cherrypy


class ServerStatus(Enum):
    """Current status of the server instance."""
    STARTED = "started"
    STOPPED = "stopped"


class Endpoint:
    """Represents a single endpoint that was added to the ``MockServer``."""

    def __init__(self, url, default_status, default_response=""):
        self.url = url
        self.default_status = default_status
        self.default_response = default_response

    @cherrypy.expose
    def index(self):
        """The index page returns the content that was specified when the endpoint was added or edited."""
        return self.default_response


class MockServer:
    """
    A ``MockServer`` handles the creation and lifecycle management of the underlying ``CherryPy`` server,
    as well as acting as an URL itself and providing endpoints to add, edit and remove andpoints.
    The underlying methods can be called from Python code directly, too.
    """

    def __init__(self, config=None):
        self.config = config or {}
        self.port = self.config.get("port", 8080)
        endpoints = self.config.get("endpoints", {})
        for endpoint, ep_config in endpoints.items():
            self.add_endpoint(endpoint, **ep_config)
        self.status = ServerStatus.STOPPED

    def start(self):
        """Start the ``CherryPy`` server with all endpoints given via the config or added through code."""
        if self.status is ServerStatus.STARTED:
            raise RuntimeError("Mock server already started, cannot start twice.")
        self.status = ServerStatus.STARTED
        cherrypy.tree.mount(self, "/__mock", {"/": {"port": self.port}})
        cherrypy.engine.start()

    def stop(self):
        """Stop and exit the ``CherryPy`` server."""
        cherrypy.engine.exit()
        self.status = ServerStatus.STOPPED

    @cherrypy.expose
    def info(self):  # pylint: disable=no-self-use
        """Returns information of all currently configured endpoints."""
        return str(cherrypy.tree.apps)

    @cherrypy.expose
    def add_endpoint(self, url, status_code=200):  # pylint: disable=no-self-use
        """Add a new endpoint at a given URL."""
        cherrypy.tree.mount(Endpoint(url=url, default_status=status_code), url)
