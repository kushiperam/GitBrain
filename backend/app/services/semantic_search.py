import re

import numpy as np

from sentence_transformers import SentenceTransformer

from app.services.code_chunker import chunk_repository


# Load embedding model once
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def search_repository(
    repository_path: str,
    question: str,
    top_k: int = 5
) -> list[dict]:
    """
    Search repository code chunks using
    semantic embedding similarity.

    Ranking improvements:
    1. Exact filename boost
    2. Prefer application code over test files
    """

    # Get repository code chunks
    chunks = chunk_repository(
        repository_path
    )

    if not chunks:
        return []

    # Create embedding for the question
    question_embedding = model.encode(
        question
    )

    # Detect explicitly mentioned filename
    mentioned_file = None

    file_matches = re.findall(
        r'[\w./\\-]+\.[a-zA-Z0-9]+',
        question
    )

    if file_matches:
        mentioned_file = (
            file_matches[0]
            .replace("\\", "/")
            .lower()
        )

    results = []

    for chunk in chunks:

        # Create embedding for code chunk
        chunk_embedding = model.encode(
            chunk["content"]
        )

        # Calculate cosine similarity
        similarity = np.dot(
            question_embedding,
            chunk_embedding
        ) / (
            np.linalg.norm(question_embedding)
            * np.linalg.norm(chunk_embedding)
        )

        real_similarity = float(
            similarity
        )

        # Ranking score starts with real similarity
        ranking_score = real_similarity

        chunk_path = str(
            chunk.get("path", "")
        ).replace("\\", "/").lower()

        # ---------------------------------
        # 1. Exact filename boost
        # ---------------------------------

        if mentioned_file:

            if (
                chunk_path.endswith(mentioned_file)
                or mentioned_file.endswith(chunk_path)
            ):
                ranking_score += 1.0

        # ---------------------------------
        # 2. Application-code boost
        # ---------------------------------

        # Test files are useful, but for broad
        # architecture questions we prefer
        # actual application implementation.

        is_test_file = (
            "/tests/" in chunk_path
            or chunk_path.startswith("tests/")
            or "/test_" in chunk_path
            or chunk_path.startswith("test_")
            or chunk_path.endswith("_test.py")
        )

        if not is_test_file:
            ranking_score += 0.15

        result = chunk.copy()

        # Show only the real similarity
        result["score"] = real_similarity

        # Internal ranking score
        result["ranking_score"] = ranking_score

        results.append(result)

    # Sort using ranking score
    results.sort(
        key=lambda item: item["ranking_score"],
        reverse=True
    )

    # Remove internal ranking score
    for result in results:
        result.pop(
            "ranking_score",
            None
        )

    return results[:top_k]