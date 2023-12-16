def test_init(client):
    resp = client.get("/")

    assert "status" in resp.json
    assert "message" in resp.json
    assert resp.json["status"] == 200
    assert resp.json["message"] == "Welcome to MEJI API"
