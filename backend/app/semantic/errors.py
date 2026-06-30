from pydantic import BaseModel, Field


class AnalysisError(BaseModel):
    type: str
    message: str
    line: int | None = Field(default=None, ge=1)
    column: int | None = Field(default=None, ge=1)
