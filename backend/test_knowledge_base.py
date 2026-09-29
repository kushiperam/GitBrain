from app.services.knowledge_base import (
    build_repository_knowledge_base
)


repository_path = "repositories/PrivacySynthAI.git"


knowledge_base = build_repository_knowledge_base(
    repository_path
)


print("================================")
print("GitBrain Knowledge Base")
print("================================")

print()

print(
    f"Total knowledge chunks: "
    f"{len(knowledge_base)}"
)

print()


for chunk in knowledge_base[:5]:

    print("--------------------------------")

    print(
        f"File: {chunk['file']}"
    )

    print(
        f"Path: {chunk['path']}"
    )

    print(
        f"Lines: "
        f"{chunk['start_line']} - "
        f"{chunk['end_line']}"
    )

    print()

    print("Content:")

    print(
        chunk["content"][:300]
    )

    print()