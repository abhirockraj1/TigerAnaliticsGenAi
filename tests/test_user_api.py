import pytest
import httpx
from app.api.schemas import user as user_schema

BASE_URL = "http://127.0.0.1:8000/api/v1"

# --- Utility function to get an access token ---
def get_access_token(client: httpx.Client, username, password):
    response = client.post(
        f"{BASE_URL}/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]

# --- Tests for /token endpoint ---
def test_login_success(client: httpx.Client):
    response = client.post(
        f"{BASE_URL}/token",
        data={"username": "abhinavK", "password": "password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_fail_incorrect_credentials(client: httpx.Client):
    response = client.post(
        f"{BASE_URL}/token",
        data={"username": "test_owner", "password": "wrong_password"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()["detail"] == "Incorrect username or password"

# --- Tests for /users/ endpoint (creating regular users by an owner) ---
def test_create_user_by_owner_success(client: httpx.Client):
    owner_token = get_access_token(client, "abhinavK", "password")
    response = client.post(
        f"{BASE_URL}/users/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {owner_token}",
        },
        json={"username": "new_collaborator", "password": "password", "role": "collaborator"},
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["username"] == "new_collaborator"
    assert response.json()["role"] == "collaborator"

def test_create_user_by_collaborator_forbidden(client: httpx.Client):
    # Assuming you have a test collaborator user
    collaborator_token = get_access_token(client, "test_collaborator", "test_password")
    response = client.post(
        f"{BASE_URL}/users/",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {collaborator_token}",
        },
        json={"username": "another_user", "password": "password", "role": "collaborator"},
    )
    assert response.status_code == 403
    assert "detail" in response.json()
    assert response.json()["detail"] == "Only owners can create users." # Adjust if your message is different


def test_get_current_collaborator_user(client: httpx.Client):
    # Assuming you have a test collaborator user
    collaborator_token = get_access_token(client, "test_collaborator", "test_password")
    response = client.get(
        f"{BASE_URL}/users/me/",
        headers={"Authorization": f"Bearer {collaborator_token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "test_collaborator"
    assert response.json()["role"] == "collaborator"

def test_get_current_user_unauthorized(client: httpx.Client):
    response = client.get(f"{BASE_URL}/users/me/")
    assert response.status_code == 401
    assert "detail" in response.json()
    assert response.json()["detail"] == "Not authenticated" # Adjust if your message is different

# --- Pytest fixture for creating an HTTP client ---
@pytest.fixture
def client():
    with httpx.Client() as client:
        yield client