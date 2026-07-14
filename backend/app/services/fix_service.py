from app.fixes.engine import FixEngine
from app.schemas.fix import ApplyFixRequest, ApplyFixResponse


class FixService:
    def apply_fix(self, request: ApplyFixRequest) -> ApplyFixResponse:
        result = FixEngine().apply(request.code, request.finding_id)
        return ApplyFixResponse(
            updatedCode=result.updated_code,
            applied=result.applied,
            message=result.message,
        )


fix_service = FixService()
