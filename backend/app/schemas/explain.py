from pydantic import BaseModel, Field

from app.schemas.common import Finding, Metrics
from app.semantic.errors import AnalysisError


class RuntimeSummaryRequest(BaseModel):
    steps: int = Field(default=0, ge=0)
    output: list[str] = Field(default_factory=list)
    final_variables: dict[str, str] = Field(
        default_factory=dict, alias="finalVariables"
    )


class ExplainRequest(BaseModel):
    code: str
    finding_id: str = Field(..., alias="findingId")
    finding: Finding | None = None
    error: AnalysisError | None = None
    metrics: Metrics | None = None
    runtime_summary: RuntimeSummaryRequest | None = Field(
        default=None, alias="runtimeSummary"
    )


class ExplainResponse(BaseModel):
    summary: str
    root_cause: str = Field(..., alias="rootCause")
    explanation: str
    how_to_fix: str = Field(..., alias="howToFix")
    corrected_example: str = Field(..., alias="correctedExample")
    learning_tip: str = Field(..., alias="learningTip")
    best_practice: str = Field(..., alias="bestPractice")
    confidence: float = Field(..., ge=0, le=1)
    unavailable: bool = False

