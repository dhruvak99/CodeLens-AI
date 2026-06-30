import builtins

from app.rules.base import BaseRule
from app.rules.models import RuleFinding
from app.semantic.models import SemanticRepresentation, SymbolInfo


BUILTIN_NAMES = set(dir(builtins))


class UndefinedVariableRule(BaseRule):
    rule_id = "UNDEF_VAR_001"
    finding_type = "undefined_variable"
    severity = "high"
    message = "Variable is referenced before it is defined in an accessible scope."

    def check(self, semantic: SemanticRepresentation) -> list[RuleFinding]:
        symbols = semantic.symbols
        findings: list[RuleFinding] = []
        reported: set[tuple[str, str]] = set()

        for reference in semantic.references:
            if reference.context != "load" or reference.name in BUILTIN_NAMES:
                continue
            key = (reference.name, reference.scope)
            if key in reported:
                continue
            if not self._is_defined(reference.name, reference.scope, symbols):
                reported.add(key)
                findings.append(
                    self.finding(
                        line=reference.line,
                        column=reference.column,
                        message=f"Variable '{reference.name}' is not defined.",
                    )
                )
        return findings

    def _is_defined(self, name: str, scope: str, symbols: list[SymbolInfo]) -> bool:
        current: str | None = scope
        while current is not None:
            if any(symbol.name == name and symbol.scope == current for symbol in symbols):
                return True
            current = current.rsplit(".", 1)[0] if "." in current else None
        return False
