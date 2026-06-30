from app.parser.ast_builder import ASTBuilder
from app.semantic.extractor import SemanticExtractor
from app.semantic.models import SemanticRepresentation


def extract_semantic(code: str) -> SemanticRepresentation:
    parse_result = ASTBuilder().parse(code)
    tree = parse_result.tree if parse_result.success else parse_result.partial_tree
    return SemanticExtractor(source=code).extract(tree)


def test_semantic_tracks_globals_locals_closures_and_scopes() -> None:
    semantic = extract_semantic(
        "global_value = 1\n"
        "def outer(x):\n"
        "    local_value = x\n"
        "    def inner():\n"
        "        return global_value + local_value\n"
        "    return inner()\n"
    )

    symbol_keys = {(symbol.scope, symbol.name) for symbol in semantic.symbols}
    scope_names = {scope.name for scope in semantic.scopes}

    assert ("global", "global_value") in symbol_keys
    assert ("global.outer", "x") in symbol_keys
    assert ("global.outer", "local_value") in symbol_keys
    assert "global.outer.inner" in scope_names


def test_semantic_tracks_classes_methods_imports_loops_and_conditionals() -> None:
    semantic = extract_semantic(
        "import math\n"
        "class Calculator:\n"
        "    def total(self, values):\n"
        "        result = 0\n"
        "        for value in values:\n"
        "            if value > 0:\n"
        "                result += value\n"
        "        return result\n"
    )

    assert any(import_info.name == "math" for import_info in semantic.imports)
    assert any(class_info.name == "Calculator" for class_info in semantic.classes)
    assert any(function.name == "total" for function in semantic.functions)
    assert any(loop.type == "for" for loop in semantic.loops)
    assert any(conditional.type == "if" for conditional in semantic.conditionals)
    assert any(edge.label == "modifies" for edge in semantic.graph.edges)


def test_semantic_supports_unicode_and_long_identifiers() -> None:
    semantic = extract_semantic(
        "π = 1\n"
        "变量 = π + 1\n"
        "very_long_variable_name = 变量 + 1\n"
        "print(very_long_variable_name)\n"
    )

    symbols = {symbol.name for symbol in semantic.symbols}

    assert "π" in symbols
    assert "变量" in symbols
    assert "very_long_variable_name" in symbols


def test_semantic_scopes_lambda_and_comprehension_variables() -> None:
    semantic = extract_semantic(
        "transform = lambda item: item + 1\n"
        "values = [item for item in range(5) if item > 1]\n"
    )

    assert any(scope.name.startswith("global.lambda_") for scope in semantic.scopes)
    assert any(
        scope.name.startswith("global.comprehension_") for scope in semantic.scopes
    )
    assert any(symbol.name == "item" for symbol in semantic.symbols)
