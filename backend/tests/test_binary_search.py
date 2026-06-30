from tests.rule_test_utils import findings_by_type


def test_detects_wrong_high_update_for_less_than_branch() -> None:
    findings = findings_by_type(
        "def search(arr, target):\n"
        "    low = 0\n"
        "    high = len(arr) - 1\n"
        "    mid = 0\n"
        "    if arr[mid] < target:\n"
        "        high = mid - 1\n",
        "binary_search_logic_issue",
    )

    assert len(findings) == 1
    assert findings[0].rule == "BIN_SEARCH_001"


def test_detects_wrong_low_update_for_greater_than_branch() -> None:
    findings = findings_by_type(
        "def search(arr, target):\n"
        "    low = 0\n"
        "    high = len(arr) - 1\n"
        "    mid = 0\n"
        "    if arr[mid] > target:\n"
        "        low = mid + 1\n",
        "binary_search_logic_issue",
    )

    assert len(findings) == 1


def test_does_not_flag_expected_binary_search_updates() -> None:
    findings = findings_by_type(
        "def search(arr, target):\n"
        "    low = 0\n"
        "    high = len(arr) - 1\n"
        "    mid = 0\n"
        "    if arr[mid] < target:\n"
        "        low = mid + 1\n"
        "    if arr[mid] > target:\n"
        "        high = mid - 1\n",
        "binary_search_logic_issue",
    )

    assert findings == []
