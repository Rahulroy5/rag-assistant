from pydantic import BaseModel


class Chunk(BaseModel):
    id: str
    text: str
    source: str
    chunk_index: int


class QueryResult(BaseModel):
    question: str
    context_chunks: list[str]
    answer: str
