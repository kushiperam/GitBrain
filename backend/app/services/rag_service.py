from app.services.semantic_search import search_repository


# Minimum similarity required before sending context to the LLM.
MIN_SIMILARITY_SCORE = 0.20


def build_rag_context(
    repository_path: str,
    question: str,
    top_k: int = 5
) -> dict:
    """
    Retrieve relevant repository code chunks
    and build context for an LLM.
    """

    results = search_repository(
        repository_path,
        question,
        top_k
    )

    # If no repository chunks were found
    if not results:
        return {
            "question": question,
            "chunks": [],
            "context": "",
            "prompt": (
                "I could not find any relevant information "
                "in the selected repository for this question."
            )
        }

    # Check the best similarity score.
    best_score = results[0]["score"]

    # Reject questions that are not sufficiently related
    # to the repository.
    if best_score < MIN_SIMILARITY_SCORE:
        return {
            "question": question,
            "chunks": [],
            "context": "",
            "prompt": (
                "I could not find relevant information "
                "in the selected repository to answer this question."
            )
        }

    context_parts = []

    for result in results:

        context_parts.append(
            f"""
File: {result['path']}
Lines: {result['start_line']} - {result['end_line']}
Similarity Score: {result['score']}

Code:
{result['content']}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are GitBrain, an AI assistant that
answers questions about software repositories.

Answer the user's question using ONLY the
repository context provided below.

If the context does not contain enough
information to answer the question, say so.

User Question:
{question}

Repository Context:
{context}

Answer:
"""

    return {
        "question": question,
        "chunks": results,
        "context": context,
        "prompt": prompt
    }


def get_rag_prompt(
    repository_path: str,
    question: str,
    top_k: int = 5
) -> str:
    """
    Return only the RAG prompt.
    """

    result = build_rag_context(
        repository_path,
        question,
        top_k
    )

    return result["prompt"]