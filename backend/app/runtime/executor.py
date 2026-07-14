from app.parser.ast_builder import ASTBuilder
from app.runtime.interpreter import RuntimeInterpreter
from app.runtime.models import RuntimeErrorType, RuntimeFault
from app.schemas.runtime import RuntimeError, RuntimeResponse


class RuntimeExecutor:
    def __init__(self, ast_builder: ASTBuilder | None = None) -> None:
        self.ast_builder = ast_builder or ASTBuilder()

    def execute(self, code: str) -> RuntimeResponse:
        parse_result = self.ast_builder.parse(code)
        if not parse_result.success or parse_result.tree is None:
            error = parse_result.error
            return RuntimeResponse(
                success=False,
                steps=[],
                output=[],
                error=RuntimeError(
                    type=RuntimeErrorType.UNSUPPORTED_SYNTAX.value,
                    message=error.message if error else "Invalid Python syntax.",
                    line=error.line if error else None,
                    column=error.column if error else None,
                ),
            )

        interpreter = RuntimeInterpreter()
        try:
            steps, output = interpreter.run(parse_result.tree)
            return RuntimeResponse(success=True, steps=steps, output=output, error=None)
        except RuntimeFault as fault:
            return RuntimeResponse(
                success=False,
                steps=[],
                output=[],
                error=RuntimeError(
                    type=fault.error_type.value,
                    message=fault.message,
                    line=fault.line,
                    column=fault.column,
                ),
            )
        except Exception as exc:
            return RuntimeResponse(
                success=False,
                steps=[],
                output=[],
                error=RuntimeError(
                    type=RuntimeErrorType.UNSUPPORTED_SYNTAX.value,
                    message=f"Runtime engine failed gracefully: {exc}",
                ),
            )

