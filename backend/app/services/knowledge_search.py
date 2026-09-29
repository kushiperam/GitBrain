from app.services.knowledge_base import (
    build_repository_knowledge_base
)


def search_repository_knowledge(
    repository_path: str,
    query: str,
    top_k: int = 5
) -> list[dict]:
    """
    Search repository knowledge using
    simple keyword matching.
    """

    knowledge_base = (
        build_repository_knowledge_base(
            repository_path
        )
    )

    query_words = {
        word.lower()
        for word in query.split()
        if len(word) > 2
    }

    results = []

    for chunk in knowledge_base:

        content = chunk["content"].lower()

        score = 0

        for word in query_words:

            if word in content:
                score += 1

        if score > 0:

            result = chunk.copy()

            result["score"] = score

            results.append(result)

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_k]