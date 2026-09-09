from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), unique=True, index=True, nullable=False)

    email = Column(String(255), unique=True, index=True, nullable=False)

    hashed_password = Column(String(255), nullable=False)

    is_active = Column(Boolean, default=True)

    is_admin = Column(Boolean, default=False)

    # `is_admin` is retained for compatibility with existing data.  New
    # authorization decisions use this explicit role instead.
    role = Column(
        String(50),
        nullable=False,
        default="developer",
        server_default="developer",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    repositories = relationship(
        "Repository",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
