"""HTTP authorization tests for repository resources against gitbrain_test only."""

from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.repository import Repository
from app.models.user import User


def create_user(db_session: Session, *, role: str = "developer") -> User:
    suffix = uuid4().hex[:12]
    user = User(
        username=f"repository_user_{suffix}",
        email=f"repository_user_{suffix}@example.com",
        hashed_password=hash_password("safe-password"),
        role=role,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def create_repository(db_session: Session, *, owner_id: int, name: str) -> Repository:
    repository = Repository(
        name=name,
        url=f"https://example.com/{name}.git",
        owner_id=owner_id,
    )
    db_session.add(repository)
    db_session.commit()
    db_session.refresh(repository)
    return repository


def authorization_header(client: TestClient, user: User) -> dict[str, str]:
    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": "safe-password"},
    )
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_owner_can_retrieve_own_repository(client: TestClient, db_session: Session):
    owner = create_user(db_session)
    repository = create_repository(db_session, owner_id=owner.id, name="owner-repository")

    response = client.get(
        f"/repositories/{repository.id}",
        headers=authorization_header(client, owner),
    )

    assert response.status_code == 200
    assert response.json()["id"] == repository.id
    assert response.json()["owner_id"] == owner.id


def test_other_user_cannot_retrieve_repository(client: TestClient, db_session: Session):
    owner = create_user(db_session)
    other_user = create_user(db_session)
    repository = create_repository(db_session, owner_id=owner.id, name="private-repository")

    response = client.get(
        f"/repositories/{repository.id}",
        headers=authorization_header(client, other_user),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Repository not found"


def test_unauthenticated_user_cannot_retrieve_repository(
    client: TestClient, db_session: Session
):
    owner = create_user(db_session)
    repository = create_repository(db_session, owner_id=owner.id, name="authenticated-only")

    response = client.get(f"/repositories/{repository.id}")

    assert response.status_code == 401


def test_repository_list_excludes_other_users_repositories(
    client: TestClient, db_session: Session
):
    owner = create_user(db_session)
    other_user = create_user(db_session)
    own_repository = create_repository(db_session, owner_id=owner.id, name="visible")
    create_repository(db_session, owner_id=other_user.id, name="hidden")

    response = client.get("/repositories/", headers=authorization_header(client, owner))

    assert response.status_code == 200
    assert [repository["id"] for repository in response.json()] == [own_repository.id]


def test_repository_creation_uses_authenticated_user_as_owner(
    client: TestClient, db_session: Session, monkeypatch
):
    owner = create_user(db_session)
    monkeypatch.setattr("app.services.repository_service.clone_repository", lambda _: "unused")
    monkeypatch.setattr("app.services.repository_service.scan_repository", lambda _: [])
    monkeypatch.setattr("app.services.repository_service.detect_languages", lambda _: {})
    monkeypatch.setattr("app.services.repository_service.detect_dependencies", lambda _: [])
    monkeypatch.setattr("app.services.repository_service.build_directory_tree", lambda _: {})

    response = client.post(
        "/repositories/",
        json={"name": "created-by-owner", "url": "https://example.com/created.git"},
        headers=authorization_header(client, owner),
    )

    assert response.status_code == 200
    assert response.json()["owner_id"] == owner.id
    assert db_session.get(Repository, response.json()["id"]).owner_id == owner.id


def test_admin_has_no_implicit_cross_owner_repository_access(
    client: TestClient, db_session: Session
):
    owner = create_user(db_session)
    admin = create_user(db_session, role="admin")
    repository = create_repository(db_session, owner_id=owner.id, name="admin-is-not-owner")

    response = client.get(
        f"/repositories/{repository.id}",
        headers=authorization_header(client, admin),
    )

    assert response.status_code == 404
