from app.rules.base import BaseRule
from app.rules.models import RuleFinding
from app.semantic.models import ScopeInfo, SemanticRepresentation, SymbolInfo


SHADOWABLE_KINDS = {"argument", "variable"}


class ShadowedVariableRule(BaseRule):
    rule_id = "SHADOWED_VAR_001"
    finding_type = "shadowed_variable"
    severity = "medium"
    message = "Variable declared in an inner scope shadows a variable from an outer scope."

    def check(self, semantic: SemanticRepresentation) -> list[RuleFinding]:
        findings: list[RuleFinding] = []
        scopes = {scope.name: scope for scope in semantic.scopes}
        symbols_by_scope = self._symbols_by_scope(semantic.symbols)
        reported: set[tuple[str, str, int]] = set()

        for symbol in semantic.symbols:
            if symbol.kind not in SHADOWABLE_KINDS or symbol.scope == "global":
                continue

            if self._scope_type(symbol.scope, scopes) == "class":
                continue

            outer = self._outer_symbol(symbol, scopes, symbols_by_scope)
            if outer is None:
                continue

            key = (symbol.name, symbol.scope, symbol.line)
            if key in reported:
                continue
            reported.add(key)
            findings.append(
                self.finding(
                    line=symbol.line,
                    column=symbol.column,
                    message=(
                        f"Variable '{symbol.name}' shadows a variable from "
                        f"outer scope '{outer.scope}'."
                    ),
                )
            )

        return findings

    def _symbols_by_scope(
        self, symbols: list[SymbolInfo]
    ) -> dict[str, dict[str, SymbolInfo]]:
        by_scope: dict[str, dict[str, SymbolInfo]] = {}
        for symbol in symbols:
            if symbol.kind not in SHADOWABLE_KINDS:
                continue
            by_scope.setdefault(symbol.scope, {}).setdefault(symbol.name, symbol)
        return by_scope

    def _outer_symbol(
        self,
        symbol: SymbolInfo,
        scopes: dict[str, ScopeInfo],
        symbols_by_scope: dict[str, dict[str, SymbolInfo]],
    ) -> SymbolInfo | None:
        scope = scopes.get(symbol.scope)
        while scope and scope.parent is not None:
            outer = symbols_by_scope.get(scope.parent, {}).get(symbol.name)
            if outer is not None:
                return outer
            scope = scopes.get(scope.parent)
        return None

    def _scope_type(
        self, scope_name: str, scopes: dict[str, ScopeInfo]
    ) -> str | None:
        scope = scopes.get(scope_name)
        return scope.type if scope else None

