from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.repository import RepositoryCreate
from app.services.repository_service import create_new_repository


router = APIRouter(
    prefix="/repositories",
    tags=["Local Repositories"],
)


@router.post(
    "/local",
)
def create_local_repository(
    repository: RepositoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if repository.source_type != "local":
        raise HTTPException(
            status_code=400,
            detail="source_type must be 'local'.",
        )

    if not repository.local_path:
        raise HTTPException(
            status_code=400,
            detail="local_path is required.",
        )

    local_path = Path(repository.local_path)

    if not local_path.exists():
        raise HTTPException(
            status_code=400,
            detail="The specified folder does not exist.",
        )

    if not local_path.is_dir():
        raise HTTPException(
            status_code=400,
            detail="The specified path is not a folder.",
        )

    try:
        return create_new_repository(
            db=db,
            repository_data=repository,
            owner_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )