from app.services.knowledge_search import (
    search_repository_knowledge
)


repository_path = "repositories/PrivacySynthAI.git"


query = "data generation"


results = search_repository_knowledge(
    repository_path,
    query
)


print("================================")
print("GitBrain Knowledge Search")
print("================================")

print()

print(
    f"Query: {query}"
)

print()

print(
    f"Results found: {len(results)}"
)

print()


for result in results:

    print("--------------------------------")

    print(
        f"File: {result['file']}"
    )

    print(
        f"Path: {result['path']}"
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

    print("Content:")

    print(
        result["content"][:500]
    )

    print()