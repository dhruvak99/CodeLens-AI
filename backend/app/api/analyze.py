from fastapi import APIRouter

from app.schemas.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.analysis_service import analysis_service

router = APIRouter(tags=["Analysis"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analyze source code",
    description=(
        "Runs parser, semantic extraction, active analyzer rules, and v1 "
        "complexity heuristics. Runtime availability remains disabled for v1."
    ),
)
def analyze_code(request: AnalyzeRequest) -> AnalyzeResponse:
    return analysis_service.analyze(request)
