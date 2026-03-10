def test_register_success(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "password" not in data  # Never expose password in response


def test_register_duplicate_email(client, registered_user):
    response = client.post("/api/v1/auth/register", json={
        "email": registered_user["email"],  # Same email
        "username": "differentuser",
        "password": "password123",
    })
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_register_duplicate_username(client, registered_user):
    response = client.post("/api/v1/auth/register", json={
        "email": "different@example.com",
        "username": registered_user["username"],  # Same username
        "password": "password123",
    })
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


def test_login_success(client, registered_user):
    response = client.post("/api/v1/auth/login", json={
        "username": registered_user["username"],
        "password": registered_user["password"],
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, registered_user):
    response = client.post("/api/v1/auth/login", json={
        "username": registered_user["username"],
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/api/v1/auth/login", json={
        "username": "ghost",
        "password": "password",
    })
    assert response.status_code == 401
