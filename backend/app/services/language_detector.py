from collections import Counter


EXTENSION_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript React",
    ".jsx": "JavaScript React",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".rb": "Ruby",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".scala": "Scala",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".json": "JSON",
    ".xml": "XML",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".md": "Markdown",
    ".sql": "SQL",
    ".sh": "Shell",
    ".dockerfile": "Docker",
}


def detect_languages(files: list[dict]) -> dict:
    """
    Detect programming languages from scanned files
    and calculate their percentages.
    """

    counter = Counter()

    for file in files:

        extension = file["extension"].lower()

        language = EXTENSION_MAP.get(
            extension,
            "Other",
        )

        counter[language] += 1

    total = sum(counter.values())

    result = {}

    for language, count in counter.items():

        percentage = round(
            (count / total) * 100,
            2,
        )

        result[language] = {
            "files": count,
            "percentage": percentage,
        }

    return result