from pydantic import BaseModel, Field


class ApplyFixRequest(BaseModel):
    code: str = Field(..., min_length=1)
    finding_id: str = Field(..., alias="findingId")


class ApplyFixResponse(BaseModel):
    updated_code: str = Field(..., alias="updatedCode")
    applied: bool
