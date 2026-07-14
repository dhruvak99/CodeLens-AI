from pydantic import BaseModel, Field


class RuntimeRequest(BaseModel):
    code: str


class RuntimeError(BaseModel):
    type: str
    message: str
    line: int | None = Field(default=None, ge=1)
    column: int | None = Field(default=None, ge=0)


class RuntimeStep(BaseModel):
    step_number: int = Field(..., alias="stepNumber", ge=1)
    line: int | None = Field(default=None, ge=1)
    executed_statement: str = Field(..., alias="executedStatement")
    changed_variable: str | None = Field(default=None, alias="changedVariable")
    variables: dict[str, str]
    output: list[str]


class RuntimeResponse(BaseModel):
    success: bool
    steps: list[RuntimeStep]
    output: list[str]
    error: RuntimeError | None = None

