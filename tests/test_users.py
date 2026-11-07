"""Tests for authenticated profile and password management."""

from tests.helpers import register_user


def test_get_current_profile(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "person@example.com"
    assert "hashed_password" not in body
    assert "password" not in body


def test_update_current_profile(client, auth_headers):
    response = client.patch(
        "/users/me",
        headers=auth_headers,
        json={"name": "Updated Name"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"


def test_update_email_to_another_users_email_returns_409(client, auth_headers):
    register_user(client, email="second@example.com")
    response = client.patch(
        "/users/me",
        headers=auth_headers,
        json={"email": "second@example.com"},
    )
    assert response.status_code == 409


def test_update_profile_rejects_empty_patch(client, auth_headers):
    response = client.patch("/users/me", headers=auth_headers, json={})
    assert response.status_code == 422


def test_change_password_and_login_with_new_password(client, registered_user, auth_headers):
    response = client.patch(
        "/users/me/password",
        headers=auth_headers,
        json={
            "current_password": "Correct-Horse-42!",
            "new_password": "New-Strong-Password-55!",
        },
    )
    assert response.status_code == 204

    old_login = client.post(
        "/auth/login",
        json={"email": "person@example.com", "password": "Correct-Horse-42!"},
    )
    new_login = client.post(
        "/auth/login",
        json={"email": "person@example.com", "password": "New-Strong-Password-55!"},
    )
    assert old_login.status_code == 401
    assert new_login.status_code == 200

    # Password changes increment the token version, invalidating prior access tokens.
    old_token_response = client.get("/users/me", headers=auth_headers)
    assert old_token_response.status_code == 401


def test_change_password_requires_current_password(client, registered_user, auth_headers):
    response = client.patch(
        "/users/me/password",
        headers=auth_headers,
        json={
            "current_password": "incorrect-current-password",
            "new_password": "New-Strong-Password-55!",
        },
    )
    assert response.status_code == 400


def test_change_password_rejects_reusing_current_password(client, registered_user, auth_headers):
    response = client.patch(
        "/users/me/password",
        headers=auth_headers,
        json={
            "current_password": "Correct-Horse-42!",
            "new_password": "Correct-Horse-42!",
        },
    )
    assert response.status_code == 400
