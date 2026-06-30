from tests.rule_test_utils import findings_by_type


def test_detects_code_after_return() -> None:
    findings = findings_by_type(
        "def f():\n"
        "    return 1\n"
        "    x = 2\n",
        "dead_code",
    )

    assert len(findings) == 1
    assert findings[0].line == 3


def test_detects_code_after_raise_break_and_continue() -> None:
    code = (
        "def f(items):\n"
        "    for item in items:\n"
        "        break\n"
        "        item = 2\n"
        "    while True:\n"
        "        continue\n"
        "        item = 3\n"
        "    raise ValueError()\n"
        "    item = 4\n"
    )

    findings = findings_by_type(code, "dead_code")

    assert [finding.line for finding in findings] == [4, 7, 9]
