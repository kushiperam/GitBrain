from git import Repo
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPOSITORIES_DIR = BASE_DIR / "repositories"


def clone_repository(repo_url: str) -> str:
    """
    Clone a GitHub repository into the repositories folder.
    Returns the local path.
    """

    REPOSITORIES_DIR.mkdir(exist_ok=True)

    repo_name = repo_url.rstrip("/").split("/")[-1]

    local_path = REPOSITORIES_DIR / repo_name

    if local_path.exists():
        return str(local_path)

    Repo.clone_from(repo_url, local_path)

    return str(local_path)