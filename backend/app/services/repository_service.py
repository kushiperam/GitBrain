from pathlib import Path

from sqlalchemy.orm import Session

from app.schemas.repository import RepositoryCreate

from app.repositories.repository_repository import (
    create_repository,
    get_repository_by_id,
    get_user_repositories,
)

from app.services.git_service import clone_repository
from app.services.file_scanner import scan_repository
from app.services.language_detector import detect_languages
from app.services.dependency_detector import detect_dependencies
from app.services.tree_builder import build_directory_tree
from app.services.repository_analyzer import analyze_repository


def create_new_repository(
    db: Session,
    repository_data: RepositoryCreate,
    owner_id: int,
):
    new_repository = create_repository(
        db,
        repository_data,
        owner_id,
    )

    # Decide where the repository is located.
    if new_repository.source_type == "local":
        if not new_repository.local_path:
            raise ValueError(
                "Local repository must have a local_path."
            )

        local_path = Path(new_repository.local_path)

        if not local_path.exists():
            raise ValueError(
                "The specified local repository path does not exist."
            )

        if not local_path.is_dir():
            raise ValueError(
                "The specified local repository path is not a folder."
            )

        print(
            "Using local repository:",
            local_path
        )

    else:
        local_path = clone_repository(
            new_repository.url
        )

        print(
            "Repository cloned:",
            local_path
        )

    files = scan_repository(
        str(local_path)
    )

    print(
        f"Scanned {len(files)} files."
    )

    languages = detect_languages(files)

    print("Languages:")
    print(languages)

    dependencies = detect_dependencies(files)

    print("Dependencies Found:")

    for dependency in dependencies:
        print(dependency)

    # Phase 21: Build Repository Directory Tree
    tree = build_directory_tree(
        str(local_path)
    )

    print("Repository Tree Created")

    print(tree)

    # Phase 22: Analyze Python source files
    analysis = analyze_repository(
        str(local_path)
    )

    print(
        f"Analyzed {len(analysis)} Python files."
    )

    for item in analysis[:5]:
        print(item)

    return new_repository


def fetch_repository(
    db: Session,
    repository_id: int,
    owner_id: int,
):
    repository = get_repository_by_id(
        db,
        repository_id,
    )

    if not repository or repository.owner_id != owner_id:
        return None

    return repository


def fetch_user_repositories(
    db: Session,
    owner_id: int,
):
    return get_user_repositories(
        db,
        owner_id,
    )