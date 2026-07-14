from pydantic import BaseModel, Field


class ApplyFixRequest(BaseModel):
    code: str
    finding_id: str = Field(..., alias="findingId")


class ApplyFixResponse(BaseModel):
    updated_code: str = Field(..., alias="updatedCode")
    applied: bool
    message: str
