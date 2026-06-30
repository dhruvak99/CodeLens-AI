from app.schemas.explain import ExplainRequest, ExplainResponse


class ExplainService:
    def explain(self, request: ExplainRequest) -> ExplainResponse:
        return ExplainResponse(
            explanation=(
                "This mock explanation describes why the selected finding matters. "
                "Real AI explanations will be added in a later implementation pass."
            )
        )


explain_service = ExplainService()
