def test_register_and_login(client):
    # register
    resp = client.post("/auth/register", json={"email":"a@x.com","username":"and","password":"pass123"})
    assert resp.status_code == 201

    resp = client.post("/auth/login", json={"email":"a@x.com","password":"pass123"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data
    # cookie should contain refresh token
    assert "refresh_token_cookie" in resp.headers.get("Set-Cookie")
