from app.ai import AIExplanationService
from app.ai.models import ExplanationContext, RuntimeSummary
from app.schemas.explain import ExplainRequest, ExplainResponse


class ExplainService:
    def __init__(self, ai_service: AIExplanationService | None = None) -> None:
        self.ai_service = ai_service or AIExplanationService()

    def explain(self, request: ExplainRequest) -> ExplainResponse:
        runtime_summary = None
        if request.runtime_summary:
            runtime_summary = RuntimeSummary(
                steps=request.runtime_summary.steps,
                output=request.runtime_summary.output,
                final_variables=request.runtime_summary.final_variables,
            )

        return self.ai_service.explain(
            ExplanationContext(
                code=request.code,
                finding_id=request.finding_id,
                finding=request.finding,
                error=request.error,
                metrics=request.metrics,
                runtime_summary=runtime_summary,
            )
        )


explain_service = ExplainService()
