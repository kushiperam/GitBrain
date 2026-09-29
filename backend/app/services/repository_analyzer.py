import os

from app.services.code_analyzer import analyze_python_file


IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    ".idea",
    ".vscode",
}


def analyze_repository(repository_path: str) -> list[dict]:
    """
    Analyze all Python files inside a repository.
    """

    results = []

    for root, dirs, files in os.walk(repository_path):

        # Ignore unnecessary directories
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORE_DIRS
        ]

        for filename in files:

            if not filename.endswith(".py"):
                continue

            full_path = os.path.join(
                root,
                filename,
            )

            result = analyze_python_file(
                full_path
            )

            # Store path relative to repository
            relative_path = os.path.relpath(
                full_path,
                repository_path,
            )

            result["path"] = relative_path

            results.append(result)

    return results