from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserResponse,
    TokenResponse
)

from app.services.user_service import (
    register_user,
    authenticate_user
)

from app.core.security import create_access_token
from app.core.auth import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    try:
        return register_user(
            db,
            user
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    authenticated_user = authenticate_user(
        db,
        form_data.username,
        form_data.password
    )

    if not authenticated_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": authenticated_user.email
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user
