from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.repository_analysis import (
    RepositoryAnalysisResponse
)

from app.services.repository_intelligence import (
    generate_repository_intelligence
)


router = APIRouter(
    prefix="/repositories",
    tags=["Repository Analysis"]
)


@router.get(
    "/{repository_id}/analysis",
    response_model=RepositoryAnalysisResponse
)
def get_repository_analysis(
    repository_id: int,
    db: Session = Depends(get_db)
):

    from app.models.repository import Repository

    repository = (
        db.query(Repository)
        .filter(Repository.id == repository_id)
        .first()
    )

    if not repository:
        raise HTTPException(
            status_code=404,
            detail="Repository not found"
        )

    repository_path = (
        "repositories/"
        + repository.name
        + ".git"
    )

    try:

        result = generate_repository_intelligence(
            repository_path
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )