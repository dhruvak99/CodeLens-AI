from tests.rule_test_utils import findings_by_type


def test_shadowed_variable_detects_function_assignment_shadowing_global() -> None:
    findings = findings_by_type(
        "x = 10\n\ndef f():\n    x = 20\n    return x\n",
        "shadowed_variable",
    )

    assert len(findings) == 1


def test_shadowed_variable_detects_nested_function_shadowing() -> None:
    findings = findings_by_type(
        "def outer():\n"
        "    value = 10\n"
        "    def inner():\n"
        "        value = 20\n"
        "        return value\n"
        "    return inner()\n"
        ,
        "shadowed_variable",
    )

    assert len(findings) == 1


def test_shadowed_variable_ignores_distinct_names() -> None:
    findings = findings_by_type(
        "total = 10\n\ndef f():\n    value = 20\n    return value\n",
        "shadowed_variable",
    )

    assert findings == []
