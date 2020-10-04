
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
