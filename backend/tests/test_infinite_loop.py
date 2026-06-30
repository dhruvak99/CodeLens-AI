from tests.rule_test_utils import findings_by_type


def test_detects_increment_moving_away_from_greater_than_condition() -> None:
    findings = findings_by_type(
        "def f(x):\n"
        "    while x > 0:\n"
        "        x += 1\n",
        "infinite_loop_risk",
    )

    assert len(findings) == 1
    assert findings[0].rule == "INF_LOOP_001"


def test_detects_decrement_moving_away_from_less_than_condition() -> None:
    findings = findings_by_type(
        "def f(x):\n"
        "    while x < 100:\n"
        "        x -= 1\n",
        "infinite_loop_risk",
    )

    assert len(findings) == 1


def test_supports_unicode_and_long_identifiers() -> None:
    code = (
        "def f(π, 变量, very_long_variable_name):\n"
        "    while π > 0:\n"
        "        π += 1\n"
        "    while 变量 < 10:\n"
        "        变量 -= 1\n"
        "    while very_long_variable_name > 0:\n"
        "        very_long_variable_name += 1\n"
    )

    assert len(findings_by_type(code, "infinite_loop_risk")) == 3


def test_does_not_flag_update_toward_termination() -> None:
    findings = findings_by_type(
        "def f(x):\n"
        "    while x > 0:\n"
        "        x -= 1\n",
        "infinite_loop_risk",
    )

    assert findings == []
