from tests.rule_test_utils import findings_by_type


def test_infinite_loop_positive_negative_and_unicode_cases() -> None:
    assert findings_by_type("x = 1\nwhile x > 0:\n    x += 1\n", "infinite_loop_risk")
    assert not findings_by_type(
        "x = 1\nwhile x > 0:\n    x -= 1\n", "infinite_loop_risk"
    )
    assert findings_by_type("π = 1\nwhile π > 0:\n    π += 1\n", "infinite_loop_risk")


def test_undefined_variable_nested_scope_edges() -> None:
    assert findings_by_type("def f():\n    print(missing)\n", "undefined_variable")
    assert not findings_by_type(
        "def outer():\n"
        "    value = 1\n"
        "    def inner():\n"
        "        return value\n"
        "    return inner()\n",
        "undefined_variable",
    )


def test_unused_variable_positive_negative_and_class_field_cases() -> None:
    assert findings_by_type("x = 10\n", "unused_variable")
    assert not findings_by_type("x = 10\nprint(x)\n", "unused_variable")
    assert not findings_by_type(
        "from dataclasses import dataclass\n@dataclass\nclass Point:\n    x: int\n",
        "unused_variable",
    )


def test_dead_and_unreachable_code_cases() -> None:
    assert findings_by_type("def f():\n    return 1\n    x = 2\n", "dead_code")
    assert findings_by_type("if False:\n    x = 1\nelse:\n    x = 2\n", "unreachable_code")
    assert not findings_by_type("if flag:\n    x = 1\nelse:\n    x = 2\n", "unreachable_code")


def test_binary_search_logic_cases() -> None:
    assert findings_by_type(
        "if arr[mid] < target:\n    high = mid - 1\n",
        "binary_search_logic_issue",
    )
    assert findings_by_type(
        "if arr[mid] > target:\n    low = mid + 1\n",
        "binary_search_logic_issue",
    )
    assert not findings_by_type(
        "if arr[mid] < target:\n    low = mid + 1\n",
        "binary_search_logic_issue",
    )


def test_missing_base_case_cases() -> None:
    assert findings_by_type("def recurse(n):\n    return recurse(n - 1)\n", "missing_base_case")
    assert not findings_by_type(
        "def recurse(n):\n"
        "    if n <= 0:\n"
        "        return 0\n"
        "    return recurse(n - 1)\n",
        "missing_base_case",
    )


def test_lambda_and_comprehension_do_not_emit_undefined_parameter_false_positives() -> None:
    code = "transform = lambda item: item + 1\nvalues = [x for x in range(3) if x]\n"

    undefined = findings_by_type(code, "undefined_variable")

    assert all("item" not in finding.message for finding in undefined)
    assert all("'x'" not in finding.message for finding in undefined)
