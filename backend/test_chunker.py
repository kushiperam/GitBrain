from app.services.code_chunker import (
    chunk_repository
)


repository_path = "repositories/PrivacySynthAI.git"


chunks = chunk_repository(
    repository_path
)


print("================================")
print("GitBrain Code Chunking")
print("================================")

print()

print(
    f"Total chunks created: {len(chunks)}"
)

print()


for chunk in chunks[:5]:

    print("--------------------------------")

    print(
        f"File: {chunk['path']}"
    )

    print(
        f"Lines: "
        f"{chunk['start_line']} - "
        f"{chunk['end_line']}"
    )

    print()

    print("Content:")

    print(
        chunk["content"][:500]
    )