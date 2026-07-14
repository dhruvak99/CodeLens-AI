from tests.rule_test_utils import findings_by_type


def test_missing_return_detects_branch_that_can_fall_through() -> None:
    findings = findings_by_type(
        "def maximum(a, b):\n"
        "    if a > b:\n"
        "        return a\n"
        "\n"
        "print(maximum(2, 1))\n"
        ,
        "missing_return",
    )

    assert len(findings) == 1


def test_missing_return_ignores_functions_with_final_return() -> None:
    findings = findings_by_type(
        "def maximum(a, b):\n"
        "    if a > b:\n"
        "        return a\n"
        "    return b\n"
        "\n"
        "print(maximum(2, 1))\n"
        ,
        "missing_return",
    )

    assert findings == []


def test_missing_return_ignores_init() -> None:
    findings = findings_by_type(
        "class Box:\n"
        "    def __init__(self, value):\n"
        "        if value > 0:\n"
        "            return None\n"
        ,
        "missing_return",
    )

    assert findings == []
