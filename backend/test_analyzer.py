from app.services.code_analyzer import analyze_python_file


file_path = "app/main.py"


result = analyze_python_file(file_path)


print(result)