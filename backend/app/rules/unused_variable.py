from app.rules.base import BaseRule
from app.rules.models import RuleFinding
from app.semantic.models import SemanticRepresentation, SymbolInfo


class UnusedVariableRule(BaseRule):
    rule_id = "UNUSED_VAR_001"
    finding_type = "unused_variable"
    severity = "medium"
    message = "Variable is assigned but never read."

    def check(self, semantic: SemanticRepresentation) -> list[RuleFinding]:
        findings: list[RuleFinding] = []
        readable_symbols = [
            symbol for symbol in semantic.symbols if symbol.kind == "variable"
        ]

        for symbol in readable_symbols:
            if symbol.name.startswith("_"):
                continue
            if self._scope_type(symbol.scope, semantic) == "class":
                continue
            if not self._has_read(symbol, semantic):
                findings.append(
                    self.finding(
                        line=symbol.line,
                        column=symbol.column,
                        message=f"Variable '{symbol.name}' is assigned but never used.",
                    )
                )
        return findings

    def _has_read(self, symbol: SymbolInfo, semantic: SemanticRepresentation) -> bool:
        for reference in semantic.references:
            if reference.context != "load" or reference.name != symbol.name:
                continue
            if reference.scope == symbol.scope or reference.scope.startswith(
                f"{symbol.scope}."
            ):
                return True
        return False

    def _scope_type(self, scope_name: str, semantic: SemanticRepresentation) -> str | None:
        for scope in semantic.scopes:
            if scope.name == scope_name:
                return scope.type
        return None
