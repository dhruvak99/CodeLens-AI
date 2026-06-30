import pytest

from app.schemas.analysis import AnalyzeRequest
from app.services.analysis_service import analysis_service


PARSER_CASES: dict[str, str] = {
    "empty_file": "",
    "comments_only": "# comment one\n# comment two\n",
    "whitespace_only": "   \n\t\n",
    "malformed_syntax": "def broken(:\n    pass",
    "incomplete_while_typing": "def f(x):\n    if x > 0:\n        return",
    "nested_functions": (
        "def outer(x):\n"
        "    y = 1\n"
        "    def inner():\n"
        "        return x + y\n"
        "    return inner()\n"
    ),
    "nested_classes": (
        "class Outer:\n"
        "    class Inner:\n"
        "        def value(self):\n"
        "            return 1\n"
    ),
    "decorators": "@decorator\ndef f():\n    return 1\n",
    "async_functions": "async def f():\n    await g()\n",
    "generators": "def numbers():\n    yield from range(3)\n",
    "comprehensions": "xs = [x for x in range(10) if x % 2]\n",
    "match_case": "match value:\n    case 1:\n        print(value)\n",
    "dataclasses": "from dataclasses import dataclass\n@dataclass\nclass P:\n    x: int\n",
    "lambda_functions": "f = lambda x: x + 1\n",
    "try_except_finally": (
        "try:\n"
        "    x = 1\n"
        "except Exception:\n"
        "    x = 2\n"
        "finally:\n"
        "    print(x)\n"
    ),
    "large_file": "\n".join(f"value_{index} = {index}" for index in range(1200)),
}


@pytest.mark.parametrize(("case_name", "code"), PARSER_CASES.items())
def test_analyzer_never_crashes_for_parser_inputs(
    case_name: str, code: str
) -> None:
    response = analysis_service.analyze(AnalyzeRequest(code=code, language="python"))

    assert response.runtime_available is False, case_name
    assert isinstance(response.findings, list), case_name
    assert isinstance(response.errors, list), case_name


def test_malformed_code_returns_structured_error_not_exception() -> None:
    response = analysis_service.analyze(
        AnalyzeRequest(code=PARSER_CASES["malformed_syntax"], language="python")
    )

    assert response.errors
    assert response.errors[0].type == "syntax_error"
