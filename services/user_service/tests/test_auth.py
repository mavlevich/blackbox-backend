import pytest
from httpx import AsyncClient


BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(base_url=BASE_URL) as ac:
        yield ac


@pytest.mark.anyio
async def test_register_user(client):
    data = {
        "email": "new@example.com",
        "username": "newuser",
        "password": "password123"
    }
    response = await client.post("/auth/register", json=data)
    assert response.status_code in (201, 409)  # ← 409 = уже существует


@pytest.mark.anyio
async def test_login_user(client):
    data = {
        "username": "new@example.com",
        "password": "password123"
    }
    response = await client.post("/auth/login", data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.anyio
async def test_get_current_user(client):
    login_response = await client.post("/auth/login", data={
        "username": "new@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"


@pytest.mark.anyio
async def test_update_user(client):
    login_response = await client.post("/auth/login", data={
        "username": "new@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.put("/auth/update", json={
        "username": "updateduser"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"


@pytest.mark.anyio
async def test_delete_user(client):
    login_response = await client.post("/auth/login", data={
        "username": "new@example.com",
        "password": "password123"
    })
    token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = await client.delete("/auth/delete", headers=headers)
    assert response.status_code in (200, 204)
