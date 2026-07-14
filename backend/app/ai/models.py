from dataclasses import dataclass

from app.schemas.common import Finding, Metrics
from app.semantic.errors import AnalysisError


@dataclass(frozen=True)
class RuntimeSummary:
    steps: int = 0
    output: list[str] | None = None
    final_variables: dict[str, str] | None = None


@dataclass(frozen=True)
class ExplanationContext:
    code: str
    finding_id: str
    finding: Finding | None = None
    error: AnalysisError | None = None
    metrics: Metrics | None = None
    runtime_summary: RuntimeSummary | None = None

