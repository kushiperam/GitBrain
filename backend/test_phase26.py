from app.services.knowledge_search import (
    search_repository_knowledge
)


repository_path = "repositories/PrivacySynthAI.git"

query = "CTGANSynthesizer"


results = search_repository_knowledge(
    repository_path,
    query,
    top_k=3
)


print("================================")
print("GitBrain Phase 26")
print("================================")

print()

print(
    f"Query: {query}"
)

print()

print(
    f"Relevant chunks found: {len(results)}"
)

print()


for result in results:

    print("--------------------------------")

    print(
        f"File: {result['file']}"
    )

    print(
        f"Lines: "
        f"{result['start_line']} - "
        f"{result['end_line']}"
    )

    print(
        f"Score: {result['score']}"
    )

    print()

    print(
        result["content"][:500]
    )

    print()