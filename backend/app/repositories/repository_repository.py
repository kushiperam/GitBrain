from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.schemas.repository import RepositoryCreate



def create_repository(
    db: Session,
    repository_data: RepositoryCreate,
    owner_id: int
):
    repository = Repository(
        name=repository_data.name,
        url=repository_data.url,
        owner_id=owner_id
    )

    db.add(repository)
    db.commit()
    db.refresh(repository)

    return repository



def get_repository_by_id(
    db: Session,
    repository_id: int
):
    return (
        db.query(Repository)
        .filter(Repository.id == repository_id)
        .first()
    )



def get_user_repositories(
    db: Session,
    owner_id: int
):
    return (
        db.query(Repository)
        .filter(Repository.owner_id == owner_id)
        .all()
    )