from app.services.repository_analyzer import analyze_repository


repository_path = "repositories/PrivacySynthAI.git"


results = analyze_repository(
    repository_path
)


print("================================")
print("GitBrain Repository Analysis")
print("================================")

print(
    f"Python files analyzed: {len(results)}"
)

print()


for result in results[:10]:

    print("--------------------------------")

    print(
        f"File: {result['path']}"
    )

    print(
        f"Lines: {result['lines']}"
    )

    print(
        f"Characters: {result['characters']}"
    )

    print(
        f"Functions: {result['functions']}"
    )

    print(
        f"Classes: {result['classes']}"
    )

    print(
        f"Imports: {result['imports']}"
    )

    print(
        f"Error: {result['error']}"
    )