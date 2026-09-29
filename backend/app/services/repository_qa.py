from app.services.llm_service import (
    generate_repository_answer
)


def answer_repository_question(
    repository_path: str,
    question: str,
) -> dict:
    """
    Answer a repository question using
    semantic search + RAG + local LLM.

    Returns both the generated answer
    and the repository source references.
    """

    result = generate_repository_answer(
        repository_path=repository_path,
        question=question,
    )

    return result