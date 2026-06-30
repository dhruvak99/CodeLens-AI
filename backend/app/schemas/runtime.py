from pydantic import BaseModel, Field


class RuntimeRequest(BaseModel):
    code: str


class RuntimeStep(BaseModel):
    step: int = Field(..., ge=1)
    line: int | None = Field(default=None, ge=1)
    statement: str


class RuntimeVariable(BaseModel):
    name: str
    value: str
    step: int = Field(..., ge=1)


class RuntimeResponse(BaseModel):
    steps: list[RuntimeStep]
    variables: list[RuntimeVariable]
    call_stack: list[str] = Field(..., alias="callStack")
