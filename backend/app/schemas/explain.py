from pydantic import BaseModel, Field


class ExplainRequest(BaseModel):
    code: str = Field(..., min_length=1)
    finding_id: str = Field(..., alias="findingId")


class ExplainResponse(BaseModel):
    explanation: str
