from app.services.semantic_search import (
    search_repository
)


repository_path = "repositories/PrivacySynthAI.git"


question = "How is synthetic data generated?"


results = search_repository(
    repository_path,
    question
)


print("================================")
print("GitBrain Semantic Search")
print("================================")

print()

print("Question:")
print(question)

print()

print(
    f"Relevant chunks found: {len(results)}"
)

print()


for result in results:

    print("--------------------------------")

    print(
        f"File: {result['path']}"
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