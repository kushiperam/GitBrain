from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.repository_qa import (
    RepositoryQuestion,
    RepositoryAnswer,
)

from app.services.repository_qa import (
    answer_repository_question,
)


router = APIRouter(
    prefix="/repositories",
    tags=["Repository Q&A"],
)


@router.post(
    "/{repository_id}/ask",
    response_model=RepositoryAnswer,
)
def ask_repository_question(
    repository_id: int,
    question: RepositoryQuestion,
    db: Session = Depends(get_db),
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
            detail="Repository not found",
        )

    # ==========================================
    # Determine repository path
    # ==========================================

    if repository.source_type == "local":

        if not repository.local_path:
            raise HTTPException(
                status_code=400,
                detail="Local repository path is missing.",
            )

        repository_path = Path(
            repository.local_path
        )

        if not repository_path.exists():
            raise HTTPException(
                status_code=400,
                detail="Local repository folder no longer exists.",
            )

        if not repository_path.is_dir():
            raise HTTPException(
                status_code=400,
                detail="Local repository path is not a folder.",
            )

        repository_path = str(
            repository_path
        )

    else:

        repository_path = (
            "repositories/"
            + repository.name
            + ".git"
        )

    # ==========================================
    # Generate repository answer
    # ==========================================

    try:

        result = answer_repository_question(
            repository_path,
            question.question,
        )

        return {
            "question": question.question,
            "answer": result["answer"],
            "sources": result["sources"],
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error