from app.services.repository_intelligence import (
    generate_repository_intelligence
)


repository_path = "repositories/PrivacySynthAI.git"


result = generate_repository_intelligence(
    repository_path
)


print("======================================")
print("       GitBrain Intelligence")
print("======================================")

print(
    f"Total Files: {result['total_files']}"
)

print(
    f"Python Files Analyzed: "
    f"{result['python_files_analyzed']}"
)

print()

print("Languages:")
print(result["languages"])

print()

print("Dependencies:")
print(result["dependencies"])