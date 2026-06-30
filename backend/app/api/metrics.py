from fastapi import APIRouter

from app.schemas.metrics import MetricsRequest, MetricsResponse
from app.services.metrics_service import metrics_service

router = APIRouter(tags=["Metrics"])


@router.post(
    "/metrics",
    response_model=MetricsResponse,
    summary="Get code metrics",
    description="Returns v1 heuristic complexity and maintainability metrics.",
)
def get_metrics(request: MetricsRequest) -> MetricsResponse:
    return metrics_service.calculate_metrics(request)
