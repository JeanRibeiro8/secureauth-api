"""Focused tests for password-hashing primitives."""

from app.core.security import hash_password, verify_password


def test_password_is_stored_as_argon2id_hash():
    password = "Strong-Password-123!"
    hashed = hash_password(password)

    assert hashed.startswith("$argon2id$")
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("Wrong-Password-123!", hashed) is False
