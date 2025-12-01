# tests/test_tasks.py
def auth_headers(client):
    """Helper: register + login and return auth header."""
    client.post("/auth/register", json={
        "email": "task@x.com",
        "username": "taskuser",
        "password": "pass123"
    })

    resp = client.post("/auth/login", json={
        "email": "task@x.com",
        "password": "pass123"
    })

    token = resp.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_task(client):
    headers = auth_headers(client)

    resp = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Testing task creation"
    }, headers=headers)

    assert resp.status_code == 201
    data = resp.get_json()
    assert data["title"] == "Test Task"


def test_get_all_tasks(client):
    headers = auth_headers(client)

    # create two tasks
    client.post("/tasks/", json={"title": "A"}, headers=headers)
    client.post("/tasks/", json={"title": "B"}, headers=headers)

    resp = client.get("/tasks/", headers=headers)
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 2


def test_get_single_task(client):
    headers = auth_headers(client)

    create = client.post("/tasks/", json={"title": "Single"}, headers=headers)
    task_id = create.get_json()["id"]

    resp = client.get(f"/tasks/{task_id}", headers=headers)
    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Single"


def test_update_task(client):
    headers = auth_headers(client)

    create = client.post("/tasks/", json={"title": "Old"}, headers=headers)
    task_id = create.get_json()["id"]

    resp = client.put(f"/tasks/{task_id}", json={
        "title": "Updated Task",
        "description": "Updated desc"
    }, headers=headers)

    assert resp.status_code == 200
    assert resp.get_json()["title"] == "Updated Task"


def test_delete_task(client):
    headers = auth_headers(client)

    create = client.post("/tasks/", json={"title": "Delete"}, headers=headers)
    task_id = create.get_json()["id"]

    resp = client.delete(f"/tasks/{task_id}", headers=headers)
    assert resp.status_code == 200

    # check it's gone
    resp2 = client.get(f"/tasks/{task_id}", headers=headers)
    assert resp2.status_code == 404
