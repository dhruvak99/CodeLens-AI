from app.schemas.runtime import RuntimeRequest, RuntimeResponse


class RuntimeService:
    def get_runtime_trace(self, request: RuntimeRequest) -> RuntimeResponse:
        return RuntimeResponse(steps=[], variables=[], callStack=[])


runtime_service = RuntimeService()
