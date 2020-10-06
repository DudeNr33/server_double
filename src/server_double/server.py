"""
Credit goes to https://gist.github.com/eruvanos/f6f62edb368a20aaa880e12976620db8 from which the basic idea is taken.
"""

from uuid import uuid4

import requests

from flask import Flask, jsonify
from threading import Thread


class MockServer(Thread):
    def __init__(self, config=None):
        super().__init__()
        config = config or {}
        self.port = config.get("port", 5000)
        self.app = Flask(__name__)
        self.url = "http://localhost:%s" % self.port

        self.app.add_url_rule("/shutdown", view_func=self._shutdown_server)

        for endpoint, config in config.get("endpoints", {}).items():
            self.add_raw_response(
                url=endpoint,
                content=config.get("content", b""),
                methods=config.get("methods", ("GET",)),
                status_code=config.get("status_code", 200)
            )

    @staticmethod
    def _shutdown_server():
        from flask import request
        if 'werkzeug.server.shutdown' not in request.environ:
            raise RuntimeError('Not running the development server')
        request.environ['werkzeug.server.shutdown']()
        return 'Server shutting down...'

    def shutdown_server(self):
        requests.get("http://localhost:%s/shutdown" % self.port)
        self.join()

    def add_callback_response(self, url, callback, methods=('GET',)):
        callback.__name__ = str(uuid4())  # change name of method to mitigate flask exception
        self.app.add_url_rule(url, view_func=callback, methods=methods)

    def add_json_response(self, url, serializable, methods=('GET',), status_code=200):
        def callback():
            return jsonify(serializable), status_code

        self.add_callback_response(url, callback, methods=methods)

    def add_raw_response(self, url, content, methods=('GET',), status_code=200):
        def callback():
            return content, status_code

        self.add_callback_response(url, callback, methods)

    def run(self):
        self.app.run(port=self.port)