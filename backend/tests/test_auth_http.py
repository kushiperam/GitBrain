"""HTTP-level authentication integration tests against gitbrain_test only."""

from uuid import uuid4

from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User


def user_payload() -> dict[str, str]:
    suffix = uuid4().hex[:12]
    return {
        "username": f"developer_{suffix}",
        "email": f"developer_{suffix}@example.com",
        "password": "safe-password",
    }


def create_user(db_session: Session, *, role: str = "developer") -> User:
    payload = user_payload()
    user = User(
        username=payload["username"],
        email=payload["email"],
        hashed_password=hash_password(payload["password"]),
        role=role,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def login(client: TestClient, email: str, password: str) -> dict[str, str]:
    response = client.post(
        "/auth/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200, response.text
    return response.json()


def authorization_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_registers_a_developer_by_default(client: TestClient):
    payload = user_payload()

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 200
    assert response.json() == {
        "id": response.json()["id"],
        "username": payload["username"],
        "email": payload["email"],
        "role": "developer",
    }


def test_register_rejects_duplicate_email(client: TestClient):
    first = user_payload()
    second = user_payload()
    second["email"] = first["email"]
    assert client.post("/auth/register", json=first).status_code == 200

    response = client.post("/auth/register", json=second)

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_register_rejects_duplicate_username(client: TestClient):
    first = user_payload()
    second = user_payload()
    second["username"] = first["username"]
    assert client.post("/auth/register", json=first).status_code == 200

    response = client.post("/auth/register", json=second)

    assert response.status_code == 409
    assert response.json()["detail"] == "Username already registered"


def test_login_returns_a_valid_bearer_token(client: TestClient):
    payload = user_payload()
    assert client.post("/auth/register", json=payload).status_code == 200

    token = login(client, payload["email"], payload["password"])

    assert token["token_type"] == "bearer"
    assert jwt.decode(
        token["access_token"],
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
    )["sub"] == payload["email"]


def test_login_rejects_invalid_password(client: TestClient, db_session: Session):
    user = create_user(db_session)

    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_rejects_nonexistent_user(client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "missing@example.com", "password": "safe-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_me_accepts_a_valid_jwt(client: TestClient, db_session: Session):
    user = create_user(db_session)
    token = login(client, user.email, "safe-password")["access_token"]

    response = client.get("/auth/me", headers=authorization_header(token))

    assert response.status_code == 200
    assert response.json()["email"] == user.email
    assert response.json()["role"] == "developer"


def test_me_rejects_a_missing_jwt(client: TestClient):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_me_rejects_an_invalid_jwt(client: TestClient):
    response = client.get("/auth/me", headers=authorization_header("not-a-jwt"))

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"


def test_admin_user_can_access_admin_users(client: TestClient, db_session: Session):
    admin = create_user(db_session, role="admin")
    token = login(client, admin.email, "safe-password")["access_token"]

    response = client.get("/admin/users", headers=authorization_header(token))

    assert response.status_code == 200
    assert response.json()[0]["email"] == admin.email
    assert response.json()[0]["role"] == "admin"


def test_developer_cannot_access_admin_users(client: TestClient, db_session: Session):
    developer = create_user(db_session)
    token = login(client, developer.email, "safe-password")["access_token"]

    response = client.get("/admin/users", headers=authorization_header(token))

    assert response.status_code == 403
    assert response.json()["detail"] == "You do not have permission to access this resource."
