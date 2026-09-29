from datetime import datetime, timezone

from app.models.user import User
from app.models.repository import Repository
from app.schemas.user import UserResponse
from app.schemas.repository import RepositoryResponse


def test_response_schemas_validate_sqlalchemy_orm_instances():
    created_at = datetime(2026, 9, 9, tzinfo=timezone.utc)

    user = User(
        id=1,
        username="schema-user",
        email="schema-user@example.com",
        hashed_password="not-exposed",
        role="developer",
    )

    repository = Repository(
        id=2,
        name="schema-repository",
        url="https://example.com/schema-repository.git",
        source_type="github",
        local_path=None,
        owner_id=user.id,
        created_at=created_at,
    )

    assert UserResponse.model_validate(user).model_dump() == {
        "id": 1,
        "username": "schema-user",
        "email": "schema-user@example.com",
        "role": "developer",
    }

    assert RepositoryResponse.model_validate(repository).model_dump() == {
        "id": 2,
        "name": "schema-repository",
        "url": "https://example.com/schema-repository.git",
        "owner_id": 1,
        "created_at": created_at,
        "source_type": "github",
        "local_path": None,
    }