from app.runtime import RuntimeExecutor
from app.schemas.runtime import RuntimeRequest, RuntimeResponse


class RuntimeService:
    def __init__(self, executor: RuntimeExecutor | None = None) -> None:
        self.executor = executor or RuntimeExecutor()

    def get_runtime_trace(self, request: RuntimeRequest) -> RuntimeResponse:
        return self.executor.execute(request.code)


runtime_service = RuntimeService()
