from tests.rule_test_utils import findings_by_type


def test_dangerous_import_detects_import() -> None:
    findings = findings_by_type("import os\nprint('ready')\n", "dangerous_import")

    assert [finding.type for finding in findings] == ["dangerous_import"]


def test_dangerous_import_detects_from_import() -> None:
    findings = findings_by_type(
        "from subprocess import Popen\nprint('ready')\n", "dangerous_import"
    )

    assert [finding.type for finding in findings] == ["dangerous_import"]


def test_dangerous_import_ignores_safe_import() -> None:
    findings = findings_by_type("import math\nprint(math.pi)\n", "dangerous_import")

    assert findings == []
