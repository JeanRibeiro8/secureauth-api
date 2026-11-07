"""Tests for registration and login."""

from datetime import datetime, timedelta, timezone

import jwt

from app.core.security import create_access_token
from tests.helpers import login_user, register_user


def test_register_user_returns_safe_profile(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "password": "Strong-Password-123!",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Ada Lovelace"
    assert body["email"] == "ada@example.com"
    assert "hashed_password" not in body
    assert "password" not in body


def test_register_duplicate_email_returns_409(client):
    register_user(client)
    response = client.post(
        "/auth/register",
        json={
            "name": "Another User",
            "email": "person@example.com",
            "password": "Another-Password-123!",
        },
    )
    assert response.status_code == 409


def test_register_invalid_payload_returns_422_without_echoing_password(client):
    response = client.post(
        "/auth/register",
        json={"name": "", "email": "not-an-email", "password": "tiny"},
    )
    assert response.status_code == 422
    assert "tiny" not in response.text


def test_login_success_returns_access_token(client, registered_user):
    response = client.post(
        "/auth/login",
        json={"email": "person@example.com", "password": "Correct-Horse-42!"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]
    assert body["expires_in"] > 0
    assert "password" not in body


def test_login_wrong_password_returns_generic_401(client, registered_user):
    response = client.post(
        "/auth/login",
        json={"email": "person@example.com", "password": "Wrong-Password-123!"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_unknown_email_returns_same_401(client):
    response = client.post(
        "/auth/login",
        json={"email": "unknown@example.com", "password": "Wrong-Password-123!"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_private_route_rejects_missing_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401


def test_private_route_rejects_invalid_token(client):
    response = client.get(
        "/users/me",
        headers={"Authorization": "Bearer not-a-real-token"},
    )
    assert response.status_code == 401


def test_private_route_rejects_expired_token(client, registered_user):
    token = create_access_token(
        subject=str(registered_user["id"]),
        expires_delta=timedelta(seconds=-5),
    )
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


def test_private_route_rejects_token_with_wrong_type(client, registered_user):
    token = jwt.encode(
        {"sub": str(registered_user["id"]), "type": "refresh", "ver": 0, "iat": datetime.now(timezone.utc), "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        "test-only-secret-key-that-is-at-least-32-characters",
        algorithm="HS256",
    )
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401


def test_health_check_reports_database_available(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}
