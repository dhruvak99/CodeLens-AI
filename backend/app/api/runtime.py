from fastapi import APIRouter

from app.schemas.runtime import RuntimeRequest, RuntimeResponse
from app.services.runtime_service import runtime_service

router = APIRouter(tags=["Runtime"])


@router.post(
    "/runtime",
    response_model=RuntimeResponse,
    summary="Get runtime trace",
    description="Runtime execution is disabled in v1 and returns an empty trace.",
)
def get_runtime_trace(request: RuntimeRequest) -> RuntimeResponse:
    return runtime_service.get_runtime_trace(request)
