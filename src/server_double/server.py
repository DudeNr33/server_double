"""
Credit goes to https://gist.github.com/eruvanos/f6f62edb368a20aaa880e12976620db8 from which the basic idea is taken.
"""

from threading import Thread
from uuid import uuid4

import requests
from flask import Flask, jsonify, request


class MockServer(Thread):
    """
    Main class for the Server Double.
    Holds a reference to the Flask application and runs it in the background.
    """

    def __init__(self, endpoint_config=None):
        super().__init__()
        endpoint_config = endpoint_config or {}
        self.port = endpoint_config.get("port", 5000)
        self.app = Flask(__name__)
        self.url = "http://localhost:%s" % self.port

        self.app.add_url_rule("/shutdown", view_func=self._shutdown_server)

        for uri, config in endpoint_config.get("endpoints", {}).items():
            self.add_raw_response(
                url=uri,
                content=config.get("content", b""),
                methods=config.get("methods", ("GET",)),
                status_code=config.get("status_code", 200)
            )

    @staticmethod
    def _shutdown_server():
        """Issue shutdown signal to the flask application."""
        if 'werkzeug.server.shutdown' not in request.environ:
            raise RuntimeError('Not running the development server')
        request.environ['werkzeug.server.shutdown']()
        return 'Server shutting down...'

    def shutdown_server(self):
        """Shuts the server down and joins the thread."""
        requests.get("http://localhost:%s/shutdown" % self.port)
        self.join()

    def add_callback_response(self, url, callback, methods=('GET',)):
        """
        Create a new endpoint which returns the value produced by the callback function.
        The callback function must return something which can be interpreted by Flask,
        i.e. either a string, or a tuple consisting of a string and an integer (for the http status code).
        """
        callback.__name__ = str(uuid4())  # change name of method to mitigate flask exception
        self.app.add_url_rule(url, view_func=callback, methods=methods)

    def add_json_response(self, url, serializable, methods=('GET',), status_code=200):
        """
        Create a new endpoint which returns a fixed value as json with the specified status_code.
        """

        def callback():
            return jsonify(serializable), status_code

        self.add_callback_response(url, callback, methods=methods)

    def add_raw_response(self, url, content, methods=('GET',), status_code=200):
        """
        Create a new endpoint which returns fixed raw content with the specified status code.
        """

        def callback():
            return content, status_code

        self.add_callback_response(url, callback, methods)

    def run(self):
        """
        Overwrite of the run method of class Thread. This starts the server.
        This method gets called when executing the start() method of this - just as for normal Thread instances in
        Python, so use MockServer().start() to actually start it.
        """
        self.app.run(port=self.port)
