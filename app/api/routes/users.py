"""Endpoints for the authenticated user's own account."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.db.models.user import User
from app.schemas.user import PasswordChange, UserResponse, UserUpdate
from app.services.auth_service import change_user_password, update_user_profile
from app.services.exceptions import (
    EmailAlreadyInUse,
    InvalidCurrentPassword,
    ReusedPassword,
)


router = APIRouter(prefix="/users", tags=["Users"])
CurrentUser = Annotated[User, Depends(get_current_user)]
DatabaseSession = Annotated[Session, Depends(get_db)]


@router.get("/me", response_model=UserResponse, summary="Get the current user's profile")
def get_my_profile(current_user: CurrentUser) -> UserResponse:
    return current_user


@router.patch("/me", response_model=UserResponse, summary="Update the current user's profile")
def update_my_profile(
    payload: UserUpdate,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> UserResponse:
    try:
        return update_user_profile(db, current_user, payload)
    except EmailAlreadyInUse:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists",
        ) from None


@router.patch(
    "/me/password",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Change the current user's password",
)
def change_my_password(
    payload: PasswordChange,
    current_user: CurrentUser,
    db: DatabaseSession,
) -> Response:
    try:
        change_user_password(db, current_user, payload)
    except InvalidCurrentPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        ) from None
    except ReusedPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from the current password",
        ) from None
    return Response(status_code=status.HTTP_204_NO_CONTENT)
