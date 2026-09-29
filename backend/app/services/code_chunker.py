import os


IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    "venv",
    ".venv",
    ".idea",
    ".vscode",
}


SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".cs",
    ".go",
    ".rs",
    ".php",
    ".rb",
    ".swift",
    ".kt",
}


def chunk_file(
    file_path: str,
    chunk_size: int = 100
) -> list[dict]:
    """
    Read a source file and split it into chunks.
    """

    chunks = []

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            lines = file.readlines()

        for start in range(
            0,
            len(lines),
            chunk_size
        ):

            chunk_lines = lines[
                start:start + chunk_size
            ]

            content = "".join(chunk_lines)

            chunks.append(
                {
                    "file": os.path.basename(
                        file_path
                    ),
                    "path": file_path,
                    "start_line": start + 1,
                    "end_line": (
                        start + len(chunk_lines)
                    ),
                    "content": content,
                }
            )

    except Exception as e:

        print(
            f"Could not read {file_path}: {e}"
        )

    return chunks


def chunk_repository(
    repository_path: str
) -> list[dict]:
    """
    Read supported source files from a repository
    and create code chunks.
    """

    all_chunks = []

    for root, dirs, files in os.walk(
        repository_path
    ):

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in IGNORE_DIRS
        ]

        for filename in files:

            extension = os.path.splitext(
                filename
            )[1].lower()

            if extension not in SUPPORTED_EXTENSIONS:
                continue

            full_path = os.path.join(
                root,
                filename
            )

            chunks = chunk_file(
                full_path
            )

            for chunk in chunks:

                chunk["path"] = os.path.relpath(
                    full_path,
                    repository_path
                )

            all_chunks.extend(chunks)

    return all_chunks