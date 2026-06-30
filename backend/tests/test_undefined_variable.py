from tests.rule_test_utils import findings_by_type


def test_detects_undefined_variable_in_call_argument() -> None:
    findings = findings_by_type("def f():\n    print(x)\n", "undefined_variable")

    assert len(findings) == 1
    assert findings[0].line == 2


def test_nested_function_can_read_parent_scope() -> None:
    findings = findings_by_type(
        "def outer():\n"
        "    value = 1\n"
        "    def inner():\n"
        "        return value\n"
        "    return inner()\n",
        "undefined_variable",
    )

    assert findings == []


def test_nested_function_reports_missing_symbol() -> None:
    findings = findings_by_type(
        "def outer():\n"
        "    def inner():\n"
        "        return missing\n"
        "    return inner()\n",
        "undefined_variable",
    )

    assert len(findings) == 1
    assert "missing" in findings[0].message


def test_class_method_scope_uses_arguments() -> None:
    findings = findings_by_type(
        "class Box:\n"
        "    def method(self):\n"
        "        return self\n",
        "undefined_variable",
    )

    assert findings == []


def test_loop_target_is_defined_but_iterable_name_is_reported() -> None:
    findings = findings_by_type(
        "for i in range(n):\n"
        "    print(i)\n",
        "undefined_variable",
    )

    assert len(findings) == 1
    assert "'n'" in findings[0].message


def test_loop_target_with_defined_iterable_has_no_undefined_findings() -> None:
    findings = findings_by_type(
        "n = 10\n"
        "for i in range(n):\n"
        "    print(i)\n",
        "undefined_variable",
    )

    assert findings == []


def test_tuple_loop_targets_are_defined_but_source_object_is_reported() -> None:
    findings = findings_by_type(
        "for key, value in data.items():\n"
        "    print(key, value)\n",
        "undefined_variable",
    )

    assert len(findings) == 1
    assert "'data'" in findings[0].message


def test_nested_loop_targets_do_not_emit_false_positives() -> None:
    findings = findings_by_type(
        "n = 10\n"
        "for i in range(n):\n"
        "    for j in range(n):\n"
        "        print(i, j)\n",
        "undefined_variable",
    )

    assert findings == []


def test_nested_loop_reports_missing_iterable_name_once() -> None:
    findings = findings_by_type(
        "for i in range(n):\n"
        "    for j in range(n):\n"
        "        print(i, j)\n",
        "undefined_variable",
    )

    assert len(findings) == 1
    assert "'n'" in findings[0].message
