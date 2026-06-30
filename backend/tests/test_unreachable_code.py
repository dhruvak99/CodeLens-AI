from tests.rule_test_utils import findings_by_type


def test_detects_constant_false_branch() -> None:
    findings = findings_by_type(
        "def f():\n"
        "    if False:\n"
        "        return 1\n"
        "    return 2\n",
        "unreachable_code",
    )

    assert len(findings) == 1
    assert findings[0].line == 3


def test_detects_constant_true_else_branch() -> None:
    findings = findings_by_type(
        "def f():\n"
        "    if True:\n"
        "        return 1\n"
        "    else:\n"
        "        return 2\n",
        "unreachable_code",
    )

    assert len(findings) == 1
    assert findings[0].line == 5
