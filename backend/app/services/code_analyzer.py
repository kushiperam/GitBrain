import ast
import os


def analyze_python_file(file_path: str) -> dict:
    """
    Analyze a Python source file and extract basic code information.
    """

    result = {
        "file": os.path.basename(file_path),
        "path": file_path,
        "lines": 0,
        "characters": 0,
        "functions": [],
        "classes": [],
        "imports": [],
        "error": None,
    }

    try:
        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:
            content = file.read()

        result["lines"] = len(content.splitlines())
        result["characters"] = len(content)

        tree = ast.parse(content)

        for node in ast.walk(tree):

            # Detect functions
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                result["functions"].append(node.name)

            # Detect classes
            elif isinstance(node, ast.ClassDef):
                result["classes"].append(node.name)

            # Detect normal imports
            elif isinstance(node, ast.Import):

                for alias in node.names:
                    result["imports"].append(alias.name)

            # Detect from ... import ...
            elif isinstance(node, ast.ImportFrom):

                if node.module:
                    result["imports"].append(node.module)

    except SyntaxError:
        result["error"] = "Invalid Python syntax"

    except Exception as e:
        result["error"] = str(e)

    return result