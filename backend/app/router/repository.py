from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryResponse,
)
from app.services.repository_service import (
    create_new_repository,
    fetch_repository,
    fetch_user_repositories,
)
from app.core.auth import get_current_user
from app.models.user import User


router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)


@router.post(
    "/",
    response_model=RepositoryResponse
)
def create_repository(
    repository: RepositoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_new_repository(
        db=db,
        repository_data=repository,
        owner_id=current_user.id,
    )


@router.get(
    "/",
    response_model=List[RepositoryResponse]
)
def get_my_repositories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return fetch_user_repositories(
        db=db,
        owner_id=current_user.id,
    )


@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse
)
def get_repository(
    repository_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repository = fetch_repository(
        db=db,
        repository_id=repository_id,
        owner_id=current_user.id,
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    return repository
