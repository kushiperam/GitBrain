DEPENDENCY_FILES = {
    "requirements.txt": "Python (pip)",
    "pyproject.toml": "Python (Poetry / PEP 621)",
    "Pipfile": "Python (Pipenv)",
    "environment.yml": "Conda",
    "package.json": "Node.js (npm)",
    "package-lock.json": "npm Lock File",
    "yarn.lock": "Yarn",
    "pnpm-lock.yaml": "pnpm",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java (Gradle)",
    "build.gradle.kts": "Kotlin Gradle",
    "Cargo.toml": "Rust (Cargo)",
    "go.mod": "Go Modules",
    "composer.json": "PHP (Composer)",
    "Gemfile": "Ruby (Bundler)",
    "Dockerfile": "Docker",
    "docker-compose.yml": "Docker Compose",
    "docker-compose.yaml": "Docker Compose",
}


def detect_dependencies(files: list[dict]) -> list[dict]:
    """
    Detect dependency and build configuration files.
    """

    dependencies = []

    for file in files:

        name = file["name"]

        if name in DEPENDENCY_FILES:

            dependencies.append(
                {
                    "file": name,
                    "technology": DEPENDENCY_FILES[name],
                    "path": file["path"],
                }
            )

    return dependencies