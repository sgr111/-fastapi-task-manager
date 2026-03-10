def test_create_task(client, auth_headers):
    response = client.post("/api/v1/tasks/", json={
        "title": "Buy groceries",
        "description": "Milk, eggs, bread",
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["is_completed"] is False


def test_create_task_unauthenticated(client):
    response = client.post("/api/v1/tasks/", json={"title": "No auth task"})
    assert response.status_code == 401


def test_list_tasks(client, auth_headers):
    # Create 2 tasks
    client.post("/api/v1/tasks/", json={"title": "Task 1"}, headers=auth_headers)
    client.post("/api/v1/tasks/", json={"title": "Task 2"}, headers=auth_headers)

    response = client.get("/api/v1/tasks/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_by_id(client, auth_headers):
    created = client.post("/api/v1/tasks/", json={"title": "Find me"}, headers=auth_headers)
    task_id = created.json()["id"]

    response = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Find me"


def test_get_task_not_found(client, auth_headers):
    response = client.get("/api/v1/tasks/9999", headers=auth_headers)
    assert response.status_code == 404


def test_update_task(client, auth_headers):
    created = client.post("/api/v1/tasks/", json={"title": "Old title"}, headers=auth_headers)
    task_id = created.json()["id"]

    response = client.put(f"/api/v1/tasks/{task_id}", json={
        "title": "New title",
        "is_completed": True,
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["is_completed"] is True


def test_delete_task(client, auth_headers):
    created = client.post("/api/v1/tasks/", json={"title": "Delete me"}, headers=auth_headers)
    task_id = created.json()["id"]

    response = client.delete(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 204

    # Confirm it's gone
    get_response = client.get(f"/api/v1/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_cannot_access_other_users_task(client, auth_headers):
    """A user should not be able to see another user's tasks."""
    # Create a task with user 1
    created = client.post("/api/v1/tasks/", json={"title": "Private task"}, headers=auth_headers)
    task_id = created.json()["id"]

    # Register and login as user 2
    client.post("/api/v1/auth/register", json={
        "email": "user2@example.com", "username": "user2", "password": "pass2"
    })
    login = client.post("/api/v1/auth/login", json={"username": "user2", "password": "pass2"})
    user2_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    # User 2 tries to access user 1's task
    response = client.get(f"/api/v1/tasks/{task_id}", headers=user2_headers)
    assert response.status_code == 404
