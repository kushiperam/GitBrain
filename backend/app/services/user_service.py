from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

from app.core.security import (
    hash_password,
    verify_password
)

from app.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_username,
)


def register_user(
    db: Session,
    user_data: UserCreate
):

    if get_user_by_email(db, user_data.email):
        raise ValueError("Email already registered")

    if get_user_by_username(db, user_data.username):
        raise ValueError("Username already registered")

    hashed_password = hash_password(
        user_data.password
    )

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role="developer"
    )

    return create_user(
        db,
        new_user
    )


def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = get_user_by_email(
        db,
        email
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user
