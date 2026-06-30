from app.parser.ast_builder import ASTBuilder
from app.semantic.extractor import SemanticExtractor
from app.semantic.models import SemanticRepresentation


def extract(code: str) -> SemanticRepresentation:
    parse_result = ASTBuilder().parse(code)
    tree = parse_result.tree if parse_result.success else parse_result.partial_tree
    return SemanticExtractor(source=code).extract(tree)


def test_extracts_functions_variables_loops_conditionals_imports_and_calls() -> None:
    semantic = extract(
        "import math\n"
        "\n"
        "def outer(arr, target):\n"
        "    low = 0\n"
        "    high = len(arr) - 1\n"
        "    while low <= high:\n"
        "        mid = (low + high) // 2\n"
        "        if arr[mid] < target:\n"
        "            low = mid + 1\n"
        "    return low\n"
    )

    assert [item.name for item in semantic.functions] == ["outer"]
    assert any(variable.name == "low" for variable in semantic.variables)
    assert any(loop.type == "while" for loop in semantic.loops)
    assert semantic.loops[0].condition_variables == ["low", "high"]
    assert "low" in semantic.loops[0].modified_variables
    assert any(item.condition == "arr[mid] < target" for item in semantic.conditionals)
    assert semantic.imports[0].name == "math"
    assert any(call.name == "len" for call in semantic.calls)
    assert semantic.graph.nodes
    assert semantic.graph.edges


def test_tracks_nested_scopes() -> None:
    semantic = extract(
        "class Box:\n"
        "    def method(self):\n"
        "        def inner(value):\n"
        "            result = value\n"
        "            return result\n"
        "        return inner(1)\n"
    )

    function_scopes = {function.name: function.scope for function in semantic.functions}
    assert function_scopes["method"] == "global.Box"
    assert function_scopes["inner"] == "global.Box.method"
    assert any(symbol.scope == "global.Box.method.inner" for symbol in semantic.symbols)
    assert any(scope.name == "global.Box.method.inner" for scope in semantic.scopes)


def test_extracts_recursion_candidates_without_generating_findings() -> None:
    semantic = extract(
        "def factorial(n):\n"
        "    if n <= 1:\n"
        "        return 1\n"
        "    return n * factorial(n - 1)\n"
    )

    assert len(semantic.recursion_candidates) == 1
    assert semantic.recursion_candidates[0].name == "factorial"
    assert semantic.errors == []


def test_handles_unusual_python_identifiers() -> None:
    semantic = extract(
        "def compute():\n"
        "    café = 1\n"
        "    Δvalue = café + 1\n"
        "    return Δvalue\n"
    )

    variable_names = {variable.name for variable in semantic.variables}
    assert {"café", "Δvalue"}.issubset(variable_names)


def test_loop_targets_are_registered_as_symbols() -> None:
    semantic = extract(
        "for a, (b, c) in something:\n"
        "    print(a, b, c)\n"
    )

    symbols = {(symbol.scope, symbol.name) for symbol in semantic.symbols}
    variables = {variable.name for variable in semantic.variables}

    assert {("global", "a"), ("global", "b"), ("global", "c")}.issubset(symbols)
    assert {"a", "b", "c"}.issubset(variables)


def test_partial_code_returns_partial_semantics_when_prefix_is_valid() -> None:
    parse_result = ASTBuilder().parse("value = 1\nif value > 0:\n    ")
    tree = parse_result.tree if parse_result.success else parse_result.partial_tree
    semantic = SemanticExtractor(source="value = 1\nif value > 0:\n    ").extract(tree)

    assert parse_result.success is False
    assert parse_result.error is not None
    assert any(variable.name == "value" for variable in semantic.variables)
