from enum import Enum

import cherrypy


class ServerStatus(Enum):
    STARTED = "started"
    STOPPED = "stopped"


class Endpoint:
    def __init__(self, url, default_status):
        self.url = url
        self.default_status = default_status

    @cherrypy.expose
    def index(self):
        return ""


class MockServer:
    def __init__(self, config=None):
        self.config = config or {}
        self.port = self.config.get("port", 8080)
        self.status = ServerStatus.STOPPED

    def start(self):
        if self.status is ServerStatus.STARTED:
            raise RuntimeError("Mock server already started, cannot start twice.")
        self.status = ServerStatus.STARTED
        cherrypy.tree.mount(self, "/__mock", {"/": {"port": self.port}})
        cherrypy.engine.start()

    def stop(self):
        cherrypy.engine.exit()
        self.status = ServerStatus.STOPPED

    @cherrypy.expose
    def info(self):
        return str(cherrypy.tree.apps)

    @cherrypy.expose
    def add_endpoint(self, url, status=200):
        cherrypy.tree.mount(Endpoint(url=url, default_status=status), url)
