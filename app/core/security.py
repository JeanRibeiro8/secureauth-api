"""Password hashing and JWT access-token helpers."""

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt import InvalidTokenError
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from app.core.config import settings


_password_hasher = PasswordHasher()  # Argon2id is the default Argon2 variant.


def hash_password(password: str) -> str:
    """Return an Argon2id password hash."""
    return _password_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a password against its stored hash."""
    try:
        return _password_hasher.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHashError, TypeError):
        return False


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    token_version: int = 0,
) -> str:
    """Create a signed JWT access token for a user ID."""
    now = datetime.now(timezone.utc)
    expires_at = now + (
        expires_delta
        if expires_delta is not None
        else timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": expires_at,
        "type": "access",
        "ver": token_version,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key.get_secret_value(),
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """Validate a JWT signature and required claims, then return its payload."""
    payload = jwt.decode(
        token,
        settings.jwt_secret_key.get_secret_value(),
        algorithms=[settings.jwt_algorithm],
        options={"require": ["sub", "iat", "exp", "type", "ver"]},
    )
    if payload.get("type") != "access":
        raise InvalidTokenError("Invalid token type")
    if not isinstance(payload.get("sub"), str) or not payload["sub"].isdigit():
        raise InvalidTokenError("Invalid token subject")
    if not isinstance(payload.get("ver"), int) or payload["ver"] < 0:
        raise InvalidTokenError("Invalid token version")
    return payload
