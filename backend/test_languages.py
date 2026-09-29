from app.services.file_scanner import scan_repository
from app.services.language_detector import detect_languages

files = scan_repository("repositories/Hello-World.git")

languages = detect_languages(files)

print(languages)