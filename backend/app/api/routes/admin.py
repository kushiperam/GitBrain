from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from app.core.permissions import admin_required

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get(
    "/users",
    response_model=List[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required)
):
    users = db.query(User).all()

    return users