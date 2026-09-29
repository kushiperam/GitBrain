from app.services.file_scanner import scan_repository

files = scan_repository("repositories/Hello-World.git")

print(f"Total files: {len(files)}")

for file in files[:10]:
    print(file)