from tests.rule_test_utils import findings_by_type


def test_detects_recursive_function_without_base_case() -> None:
    findings = findings_by_type(
        "def recurse(n):\n"
        "    return recurse(n - 1)\n",
        "missing_base_case",
    )

    assert len(findings) == 1
    assert findings[0].rule == "RECURSION_001"


def test_does_not_flag_recursive_function_with_conditional_base_case() -> None:
    findings = findings_by_type(
        "def recurse(n):\n"
        "    if n <= 0:\n"
        "        return 0\n"
        "    return recurse(n - 1)\n",
        "missing_base_case",
    )

    assert findings == []


def test_multiple_functions_only_flags_missing_base_case() -> None:
    findings = findings_by_type(
        "def ok(n):\n"
        "    if n <= 0:\n"
        "        return 0\n"
        "    return ok(n - 1)\n"
        "\n"
        "def bad(n):\n"
        "    return bad(n - 1)\n",
        "missing_base_case",
    )

    assert len(findings) == 1
    assert findings[0].line == 7
