#!/usr/bin/env python

"""Tests for `flask_mock_server` package."""
import time

import pytest
import requests

from click.testing import CliRunner

from flask_mock_server import cli
from flask_mock_server.flask_mock_server import MockServer


@pytest.fixture
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


def test_callback_response(mock_server):
    uri = "/callback"
    expected_response = "Hello World!"

    def callback():
        return expected_response

    mock_server.add_callback_response(uri, callback)

    actual_response = requests.get(mock_server.url + uri).text

    assert actual_response == expected_response


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'flask_mock_server.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
