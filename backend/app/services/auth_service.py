from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.security import hash_password


class AuthService:

    def __init__(self):
        self.repo = UserRepository()

    def register(self, db: Session, user_data: UserCreate):

        existing = self.repo.get_by_email(db, user_data.email)

        if existing:
            raise ValueError("Email already registered")

        user = User(
            username=user_data.username,
            email=user_data.email,
            password=hash_password(user_data.password)
        )

        return self.repo.create(db, user)