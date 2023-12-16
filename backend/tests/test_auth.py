

def test_auth(client):
    token = None

    resp = client.post(
        "/init",
        headers={
            "Authorization": "qqqq"
        }
    )

    assert "status" in resp.json
    assert "user" in resp.json
    assert "token" in resp.json
    assert resp.json["status"] == 200

    if "user" in resp.json:
        token = resp.json["token"]

    resp = client.post(
        "/user",
        headers={
            "Authorization": token
        }
    )

    assert "status" in resp.json
    assert "error" in resp.json
    assert resp.json["status"] == 400
    assert resp.json["error"] == "invalid request"


def test_signup_error_01(client):
    resp = client.post(
        "/user",
        headers={
            "Authorization": "qqq"
        }
    )

    assert "status" in resp.json
    assert "error" in resp.json
    assert resp.json["status"] == 400
    assert resp.json["error"] == "invalid token"
