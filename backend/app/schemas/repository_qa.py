from pydantic import BaseModel


class RepositoryQuestion(BaseModel):
    question: str


class RepositorySource(BaseModel):
    file: str
    start_line: int
    end_line: int
    score: float


class RepositoryAnswer(BaseModel):
    question: str
    answer: str
    sources: list[RepositorySource]