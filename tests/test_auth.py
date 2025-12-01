# tests/test_auth.py
# Test register with msg as response
# def test_register(client):
#     resp = client.post("/auth/register", json={
#         "email": "test@example.com",
#         "username": "testuser",
#         "password": "pass123"
#     })

#     assert resp.status_code == 201
#     data = resp.get_json()
#     assert data["msg"].lower().startswith("user created")

def test_register(client):
    resp = client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "pass123"
    })

    assert resp.status_code == 201
    data = resp.get_json()

    # Validar los campos reales que devuelve tu API
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert data["role"] == "user"
    assert "id" in data


def test_login(client):
    # register first
    client.post("/auth/register", json={
        "email": "test2@example.com",
        "username": "test2",
        "password": "pass123"
    })

    resp = client.post("/auth/login", json={
        "email": "test2@example.com",
        "password": "pass123"
    })

    assert resp.status_code == 200
    data = resp.get_json()
    assert "access_token" in data

    # check refresh token cookie
    cookies = resp.headers.get("Set-Cookie")
    assert "refresh_token_cookie" in cookies


def test_protected_with_access_token(client):
    # register + login
    client.post("/auth/register", json={
        "email": "test3@example.com",
        "username": "test3",
        "password": "pass123"
    })
    resp = client.post("/auth/login", json={
        "email": "test3@example.com",
        "password": "pass123"
    })

    access = resp.get_json()["access_token"]

    # now request a protected endpoint
    resp2 = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {access}"}
    )

    assert resp2.status_code == 200


def test_refresh_token(client):
    client.post("/auth/register", json={
        "email": "test4@example.com",
        "username": "test4",
        "password": "pass123"
    })

    login = client.post("/auth/login", json={
        "email": "test4@example.com",
        "password": "pass123"
    })

    # The client will automatically store cookies
    refresh_resp = client.post("/auth/refresh")

    assert refresh_resp.status_code == 200
    assert "access_token" in refresh_resp.get_json()


def test_logout(client):
    client.post("/auth/register", json={
        "email": "test5@example.com",
        "username": "test5",
        "password": "pass123"
    })

    client.post("/auth/login", json={
        "email": "test5@example.com",
        "password": "pass123"
    })

    resp = client.post("/auth/logout")
    assert resp.status_code == 200

    # cookie should be cleared
    cookies = resp.headers.get("Set-Cookie")
    assert "expires=Thu, 01 Jan 1970" in cookies
