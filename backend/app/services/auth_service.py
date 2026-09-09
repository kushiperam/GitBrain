from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.services.user_service import register_user


class AuthService:
    """Compatibility facade for the original service-oriented auth API."""

    def register(self, db: Session, user_data: UserCreate):
        return register_user(db, user_data)
