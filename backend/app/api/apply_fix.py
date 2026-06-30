from fastapi import APIRouter

from app.schemas.fix import ApplyFixRequest, ApplyFixResponse
from app.services.fix_service import fix_service

router = APIRouter(tags=["Fixes"])


@router.post(
    "/apply-fix",
    response_model=ApplyFixResponse,
    summary="Apply a suggested fix",
    description=(
        "Returns the submitted code unchanged with applied=false. Real code action "
        "application is intentionally not implemented yet."
    ),
)
def apply_fix(request: ApplyFixRequest) -> ApplyFixResponse:
    return fix_service.apply_fix(request)
