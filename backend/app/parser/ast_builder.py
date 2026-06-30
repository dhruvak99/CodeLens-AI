import ast
from dataclasses import dataclass

from app.semantic.errors import AnalysisError


@dataclass(frozen=True)
class ParseResult:
    success: bool
    tree: ast.Module | None = None
    error: AnalysisError | None = None
    partial_tree: ast.Module | None = None

    def to_contract(self) -> dict[str, object]:
        if self.success:
            return {"success": True, "ast": self.tree}

        return {
            "success": False,
            "error": self.error.model_dump() if self.error else None,
        }


class ASTBuilder:
    def parse(self, code: str) -> ParseResult:
        try:
            tree = ast.parse(code or "")
            return ParseResult(success=True, tree=tree)
        except SyntaxError as exc:
            return ParseResult(
                success=False,
                error=self._syntax_error(exc),
                partial_tree=self._parse_prefix(code, exc.lineno),
            )
        except Exception as exc:  # Defensive boundary for editor-time input.
            return ParseResult(
                success=False,
                error=AnalysisError(type="parse_error", message=str(exc)),
            )

    def _syntax_error(self, exc: SyntaxError) -> AnalysisError:
        return AnalysisError(
            type="syntax_error",
            message=exc.msg or "Invalid Python syntax.",
            line=exc.lineno,
            column=exc.offset,
        )

    def _parse_prefix(self, code: str, error_line: int | None) -> ast.Module | None:
        if not error_line or error_line <= 1:
            return None

        lines = code.splitlines()
        prefix = "\n".join(lines[: error_line - 1]).rstrip()
        if not prefix:
            return None

        while prefix:
            try:
                return ast.parse(prefix)
            except SyntaxError:
                prefix = "\n".join(prefix.splitlines()[:-1]).rstrip()
            except Exception:
                return None

        return None
