from app.services.rag_service import build_rag_context


repository_path = "repositories/PrivacySynthAI.git"

question = "How is synthetic data generated?"


result = build_rag_context(
    repository_path,
    question,
    top_k=1
)


print("================================")
print("GitBrain RAG Verification")
print("================================")

print()

print("Question:")
print(question)

print()

print(
    "Retrieved chunks:",
    len(result["chunks"])
)

print()

if result["chunks"]:

    best_chunk = result["chunks"][0]

    print("================================")
    print("BEST MATCH")
    print("================================")

    print()

    print("File:")
    print(best_chunk["path"])

    print()

    print("Similarity:")
    print(best_chunk["score"])

    print()

    print("Code:")
    print(best_chunk["content"])

else:

    print("No relevant repository code found.")