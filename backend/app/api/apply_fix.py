from fastapi import APIRouter

from app.schemas.fix import ApplyFixRequest, ApplyFixResponse
from app.services.fix_service import fix_service

router = APIRouter(tags=["Fixes"])


@router.post(
    "/apply-fix",
    response_model=ApplyFixResponse,
    summary="Apply a suggested fix",
    description=(
        "Applies deterministic rule-based code actions when the requested finding "
        "still matches the submitted code."
    ),
)
def apply_fix(request: ApplyFixRequest) -> ApplyFixResponse:
    return fix_service.apply_fix(request)
