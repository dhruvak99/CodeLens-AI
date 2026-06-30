from collections import defaultdict

from app.semantic.models import SymbolInfo


class SymbolTable:
    def __init__(self) -> None:
        self._symbols: dict[str, dict[str, SymbolInfo]] = defaultdict(dict)

    def define(self, symbol: SymbolInfo) -> None:
        self._symbols[symbol.scope][symbol.name] = symbol

    def symbols(self) -> list[SymbolInfo]:
        result: list[SymbolInfo] = []
        for scoped_symbols in self._symbols.values():
            result.extend(scoped_symbols.values())
        return result

    def scope_names(self) -> list[str]:
        return list(self._symbols.keys())
