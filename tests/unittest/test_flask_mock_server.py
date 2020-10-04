import pytest

from click.testing import CliRunner

from flask_mock_server import cli
from flask_mock_server.flask_mock_server import MockServer


@pytest.fixture
def server():
    return MockServer()


@pytest.fixture
def client(server):
    app = server.app
    yield app.test_client()


def test_add_json_response(server, client):
    uri = "/json"
    expected_response = ["hello", "world"]
    server.add_json_response(
        url=uri,
        serializable=expected_response
    )

    actual_response = client.get(server.url + uri).json

    assert actual_response == expected_response


def test_add_callback_response(server, client):
    uri = "/callback"
    expected_response = b"Hello World!"

    def callback():
        return expected_response

    server.add_callback_response(uri, callback)

    actual_response = client.get(server.url + uri).data

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
