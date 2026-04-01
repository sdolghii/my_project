import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_root():
    # Строка 10, 17, 29 — заменить на:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, FastAPI!"}

@pytest.mark.asyncio
async def test_register():
    # Строка 10, 17, 29 — заменить на:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/register", json={
            "name": "Test User",
            "age": 25,
            "email": "test@test.com",
            "password": "testpass123"
        })
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_users_without_token():
    # Строка 10, 17, 29 — заменить на:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/users")
    assert response.status_code == 401