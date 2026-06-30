from app.schemas.fix import ApplyFixRequest, ApplyFixResponse


class FixService:
    def apply_fix(self, request: ApplyFixRequest) -> ApplyFixResponse:
        return ApplyFixResponse(updatedCode=request.code, applied=False)


fix_service = FixService()
