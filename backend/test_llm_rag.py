from app.services.rag_service import (
    build_rag_context
)

from app.services.llm_service import (
    generate_answer
)


# ==========================================
# GitBrain Repository
# ==========================================

repository_path = (
    "repositories/PrivacySynthAI.git"
)


# ==========================================
# User Question
# ==========================================

question = (
    "How is synthetic data generated?"
)


print("================================")
print("GitBrain LLM + RAG Test")
print("================================")

print()

print("Question:")
print(question)

print()


# ==========================================
# Step 1 — Build RAG Context
# ==========================================

print("Building RAG context...")

rag_result = build_rag_context(
    repository_path,
    question,
    top_k=5
)


print(
    f"Retrieved chunks: "
    f"{len(rag_result['chunks'])}"
)

print()


# ==========================================
# Step 2 — Generate Answer
# ==========================================

print("Generating answer...")
print()

answer = generate_answer(
    question=question,
    context=rag_result["context"],
    max_new_tokens=200
)


# ==========================================
# Step 3 — Display Answer
# ==========================================

print("================================")
print("GitBrain Answer")
print("================================")

print()

print(answer)

print()

print("================================")
print("RAG + LLM Test Complete")
print("================================")