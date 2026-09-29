from app.services.code_chunker import (
    chunk_repository
)


def build_repository_knowledge_base(
    repository_path: str
) -> list[dict]:
    """
    Build a simple repository knowledge base
    from source-code chunks.
    """

    chunks = chunk_repository(
        repository_path
    )

    knowledge_base = []

    for chunk in chunks:

        knowledge_base.append(
            {
                "file": chunk["file"],
                "path": chunk["path"],
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"],
                "content": chunk["content"],
            }
        )

    return knowledge_base