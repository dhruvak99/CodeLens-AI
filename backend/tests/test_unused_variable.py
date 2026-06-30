from tests.rule_test_utils import findings_by_type


def test_detects_assigned_variable_never_read() -> None:
    findings = findings_by_type("def f():\n    x = 10\n    return 1\n", "unused_variable")

    assert len(findings) == 1
    assert findings[0].rule == "UNUSED_VAR_001"


def test_does_not_flag_read_variable() -> None:
    findings = findings_by_type("def f():\n    x = 10\n    return x\n", "unused_variable")

    assert findings == []


def test_supports_unicode_variable_usage() -> None:
    findings = findings_by_type(
        "def f():\n"
        "    变量 = 10\n"
        "    return 变量\n",
        "unused_variable",
    )

    assert findings == []
