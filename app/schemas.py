from typing import Any

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    prompt: str = Field(min_length=1)
    session_id: str | None = None


class Citation(BaseModel):
    generated_response_part: dict[str, Any] | None = None
    retrieved_references: list[dict[str, Any]] = Field(default_factory=list)


class QueryResponse(BaseModel):
    answer: str
    session_id: str | None = None
    citations: list[Citation] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
