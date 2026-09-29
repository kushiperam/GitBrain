from app.services.file_scanner import scan_repository
from app.services.dependency_detector import detect_dependencies

files = scan_repository("repositories/Hello-World.git")

dependencies = detect_dependencies(files)

for dependency in dependencies:
    print(dependency)