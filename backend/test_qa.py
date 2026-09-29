from app.services.repository_qa import (
    answer_repository_question
)


repository_path = "repositories/Hello-World.git"


question = "Explain the project structure."


answer = answer_repository_question(
    repository_path,
    question
)


print("================================")
print("GitBrain Repository Q&A")
print("================================")

print()

print("Question:")
print(question)

print()

print("Answer:")
print(answer)