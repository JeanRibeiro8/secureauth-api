"""Business logic for registration, login, and account management."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.db.models.user import User
from app.repositories import user_repository
from app.schemas.user import PasswordChange, UserRegister, UserUpdate
from app.services.exceptions import (
    EmailAlreadyInUse,
    EmailAlreadyRegistered,
    InvalidCredentials,
    InvalidCurrentPassword,
    ReusedPassword,
)


def register_user(db: Session, data: UserRegister) -> User:
    email = str(data.email).lower()
    if user_repository.get_by_email(db, email):
        raise EmailAlreadyRegistered

    user = User(
        name=data.name,
        email=email,
        hashed_password=hash_password(data.password),
        is_active=True,
    )
    try:
        return user_repository.create(db, user)
    except IntegrityError as exc:
        db.rollback()
        raise EmailAlreadyRegistered from exc


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = user_repository.get_by_email(db, email.lower())
    # Use the same public error for unknown email and wrong password.
    if user is None or not verify_password(password, user.hashed_password):
        raise InvalidCredentials
    if not user.is_active:
        raise InvalidCredentials
    return user


def issue_access_token(user: User) -> str:
    return create_access_token(subject=str(user.id), token_version=user.token_version)


def update_user_profile(db: Session, user: User, data: UserUpdate) -> User:
    changes = data.model_dump(exclude_unset=True)

    if "email" in changes:
        new_email = str(changes["email"]).lower()
        existing = user_repository.get_by_email(db, new_email)
        if existing is not None and existing.id != user.id:
            raise EmailAlreadyInUse
        user.email = new_email

    if "name" in changes:
        user.name = changes["name"]

    try:
        return user_repository.save(db, user)
    except IntegrityError as exc:
        db.rollback()
        raise EmailAlreadyInUse from exc


def change_user_password(db: Session, user: User, data: PasswordChange) -> None:
    if not verify_password(data.current_password, user.hashed_password):
        raise InvalidCurrentPassword
    if verify_password(data.new_password, user.hashed_password):
        raise ReusedPassword

    user.hashed_password = hash_password(data.new_password)
    # Invalidate access tokens created before this password change.
    user.token_version += 1
    user_repository.save(db, user)
