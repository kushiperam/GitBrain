from typing import Any

from pydantic import BaseModel


class RepositoryAnalysisResponse(BaseModel):

    total_files: int

    languages: dict[str, Any]

    dependencies: list[dict[str, Any]]

    directory_tree: dict[str, Any]

    python_files_analyzed: int

    code_analysis: list[dict[str, Any]]