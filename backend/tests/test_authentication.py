import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi import HTTPException
from jose import jwt

# Import both mapped classes before constructing a User, so SQLAlchemy can
# resolve the relationship declared on User.
from app.models.repository import Repository  # noqa: F401
from app.models.user import User
from app.schemas.user import UserCreate
from app.services.user_service import authenticate_user, register_user
from app.core.auth import get_current_user
from app.core.permissions import admin_required
from app.core.security import create_access_token, hash_password
from app.core.config import settings
from app.api.routes.auth import get_me, login, register


class FakeQuery:
    def __init__(self, result):
        self.result = result

    def filter(self, *args):
        return self

    def first(self):
        return self.result


class FakeSession:
    def __init__(self, result=None):
        self.result = result

    def query(self, *args):
        return FakeQuery(self.result)


class UserAuthenticationTests(unittest.TestCase):
    def test_user_model_accepts_a_role(self):
        user = User(
            username="new-user",
            email="new-user@example.com",
            hashed_password="hash",
            role="developer",
        )
        self.assertEqual(user.role, "developer")

    def test_registration_assigns_developer_role_and_hashes_password(self):
        created = []

        def save_user(db, user):
            created.append(user)
            return user

        with (
            patch("app.services.user_service.get_user_by_email", return_value=None),
            patch("app.services.user_service.get_user_by_username", return_value=None),
            patch("app.services.user_service.create_user", side_effect=save_user),
        ):
            user = register_user(
                FakeSession(),
                UserCreate(
                    username="new-user",
                    email="new-user@example.com",
                    password="safe-password",
                ),
            )

        self.assertEqual(created, [user])
        self.assertEqual(user.role, "developer")
        self.assertNotEqual(user.hashed_password, "safe-password")

    def test_registration_rejects_duplicate_email(self):
        with patch(
            "app.services.user_service.get_user_by_email",
            return_value=SimpleNamespace(),
        ):
            with self.assertRaisesRegex(ValueError, "Email already registered"):
                register_user(
                    FakeSession(),
                    UserCreate(
                        username="new-user",
                        email="new-user@example.com",
                        password="safe-password",
                    ),
                )

    def test_registration_endpoint_returns_conflict_for_duplicate_user(self):
        with patch(
            "app.api.routes.auth.register_user",
            side_effect=ValueError("Email already registered"),
        ):
            with self.assertRaises(HTTPException) as error:
                register(
                    UserCreate(
                        username="new-user",
                        email="new-user@example.com",
                        password="safe-password",
                    ),
                    FakeSession(),
                )
        self.assertEqual(error.exception.status_code, 409)

    def test_login_returns_a_bearer_token_for_valid_credentials(self):
        user = SimpleNamespace(email="user@example.com")
        form = SimpleNamespace(username="user@example.com", password="safe-password")
        with patch("app.api.routes.auth.authenticate_user", return_value=user):
            response = login(form, FakeSession())

        self.assertEqual(response["token_type"], "bearer")
        self.assertEqual(
            jwt.decode(
                response["access_token"],
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )["sub"],
            user.email,
        )

    def test_authentication_service_accepts_valid_password(self):
        user = SimpleNamespace(
            email="user@example.com",
            hashed_password=hash_password("safe-password"),
        )
        with patch("app.services.user_service.get_user_by_email", return_value=user):
            self.assertIs(authenticate_user(FakeSession(), user.email, "safe-password"), user)

    def test_jwt_resolves_current_user(self):
        user = SimpleNamespace(email="user@example.com", role="developer")
        token = create_access_token({"sub": user.email})

        self.assertIs(get_current_user(token, FakeSession(user)), user)

    def test_auth_me_returns_the_authenticated_user(self):
        user = SimpleNamespace(email="user@example.com", role="developer")
        self.assertIs(get_me(user), user)

    def test_admin_authorization_uses_role(self):
        admin = SimpleNamespace(role="admin")
        self.assertIs(admin_required(admin), admin)
        with self.assertRaises(HTTPException) as error:
            admin_required(SimpleNamespace(role="developer"))
        self.assertEqual(error.exception.status_code, 403)
