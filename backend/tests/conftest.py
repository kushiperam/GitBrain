"""Safe, isolated database fixtures for HTTP integration tests."""

from collections.abc import Iterator
from pathlib import Path
import os

import pytest
from dotenv import dotenv_values
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import Session, sessionmaker

from app.db.session import Base, get_db
from app.models.repository import Repository
from app.models.user import User


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_DATABASE_NAME = "gitbrain_test"


def _validated_test_database_url() -> URL:
    raw_url = os.environ.get("GITBRAIN_TEST_DATABASE_URL")
    if not raw_url:
        pytest.fail(
            "GITBRAIN_TEST_DATABASE_URL must be set before running integration tests. "
            "Tests will not infer or use DATABASE_URL."
        )

    url = make_url(raw_url)
    if not url.drivername.startswith("postgresql"):
        pytest.fail("Integration tests require a PostgreSQL GITBRAIN_TEST_DATABASE_URL.")
    if url.database != TEST_DATABASE_NAME:
        pytest.fail(
            f"Refusing to use database {url.database!r}; only {TEST_DATABASE_NAME!r} is allowed."
        )

    development_url = dotenv_values(PROJECT_ROOT / ".env").get("DATABASE_URL")
    if development_url and make_url(development_url).render_as_string(hide_password=False) == url.render_as_string(hide_password=False):
        pytest.fail("GITBRAIN_TEST_DATABASE_URL matches the development DATABASE_URL.")

    return url


@pytest.fixture(scope="session")
def test_engine():
    """Create schema only in the explicitly validated test database."""
    engine = create_engine(_validated_test_database_url(), future=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    engine.dispose()


@pytest.fixture(autouse=True)
def clean_test_database(test_engine) -> Iterator[None]:
    """Delete only test rows, after the database-name safety check has passed."""
    with Session(test_engine) as session:
        session.execute(delete(Repository))
        session.execute(delete(User))
        session.commit()
    yield
    with Session(test_engine) as session:
        session.execute(delete(Repository))
        session.execute(delete(User))
        session.commit()


@pytest.fixture
def db_session(test_engine) -> Iterator[Session]:
    session = sessionmaker(bind=test_engine, autocommit=False, autoflush=False)()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session: Session) -> Iterator[TestClient]:
    from app.main import app

    def override_get_db() -> Iterator[Session]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
