from fastapi import APIRouter

from app.schemas.explain import ExplainRequest, ExplainResponse
from app.services.explain_service import explain_service

router = APIRouter(tags=["Explanation"])


@router.post(
    "/explain",
    response_model=ExplainResponse,
    summary="Explain a finding",
    description=(
        "Uses local Ollama to explain existing analyzer output. The AI layer "
        "does not detect bugs, calculate complexity, or decide fixes."
    ),
)
def explain_finding(request: ExplainRequest) -> ExplainResponse:
    return explain_service.explain(request)
