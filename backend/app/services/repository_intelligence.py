from app.services.file_scanner import scan_repository
from app.services.language_detector import detect_languages
from app.services.dependency_detector import detect_dependencies
from app.services.tree_builder import build_directory_tree
from app.services.repository_analyzer import analyze_repository


def generate_repository_intelligence(repository_path: str) -> dict:
    """
    Generate a complete intelligence report for a repository.
    """

    # 1. Scan files
    files = scan_repository(repository_path)

    # 2. Detect languages
    languages = detect_languages(files)

    # 3. Detect dependencies
    dependencies = detect_dependencies(files)

    # 4. Build directory tree
    tree = build_directory_tree(repository_path)

    # 5. Analyze source code
    code_analysis = analyze_repository(repository_path)

    return {
        "total_files": len(files),
        "languages": languages,
        "dependencies": dependencies,
        "directory_tree": tree,
        "python_files_analyzed": len(code_analysis),
        "code_analysis": code_analysis,
    }