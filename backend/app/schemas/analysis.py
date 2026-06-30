from pydantic import BaseModel, Field

from app.schemas.common import Finding, Language, Metrics, SemanticGraph
from app.semantic.errors import AnalysisError


class AnalyzeRequest(BaseModel):
    code: str
    language: Language


class AnalyzeResponse(BaseModel):
    findings: list[Finding]
    semantic_graph: SemanticGraph = Field(..., alias="semanticGraph")
    metrics: Metrics
    runtime_available: bool = Field(..., alias="runtimeAvailable")
    errors: list[AnalysisError] = Field(default_factory=list)
