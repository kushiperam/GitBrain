import os
from typing import List


IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".idea",
    ".vscode",
    "node_modules",
    "venv",
    ".venv",
}


def scan_repository(repository_path: str) -> List[dict]:
    """
    Scan a repository and collect metadata for every file.
    """

    files = []

    for root, dirs, filenames in os.walk(repository_path):

        # Ignore unnecessary directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

        for filename in filenames:

            full_path = os.path.join(root, filename)

            relative_path = os.path.relpath(
                full_path,
                repository_path,
            )

            extension = os.path.splitext(filename)[1]

            size = os.path.getsize(full_path)

            files.append(
                {
                    "name": filename,
                    "path": relative_path,
                    "extension": extension,
                    "size": size,
                }
            )

    return files