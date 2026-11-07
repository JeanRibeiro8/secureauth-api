"""Reusable HTTP helpers for API tests."""

from fastapi.testclient import TestClient


def register_user(client: TestClient, email: str = "person@example.com") -> dict:
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "Correct-Horse-42!",
        },
    )
    assert response.status_code == 201
    return response.json()


def login_user(client: TestClient, email: str = "person@example.com") -> str:
    response = client.post(
        "/auth/login",
        json={"email": email, "password": "Correct-Horse-42!"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]
