from fastapi import APIRouter

from app.schemas.runtime import RuntimeRequest, RuntimeResponse
from app.services.runtime_service import runtime_service

router = APIRouter(tags=["Runtime"])


@router.post(
    "/runtime",
    response_model=RuntimeResponse,
    summary="Get runtime trace",
    description=(
        "Safely interpret a restricted Python AST subset and return execution "
        "steps, captured output, or a structured runtime error."
    ),
)
def get_runtime_trace(request: RuntimeRequest) -> RuntimeResponse:
    return runtime_service.get_runtime_trace(request)
