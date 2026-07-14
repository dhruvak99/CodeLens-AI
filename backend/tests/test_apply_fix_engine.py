from app.schemas.analysis import AnalyzeRequest
from app.schemas.fix import ApplyFixRequest
from app.services.analysis_service import analysis_service
from app.services.fix_service import fix_service


def apply_first_fix(code: str, finding_type: str) -> dict[str, object]:
    analysis = analysis_service.analyze(
        AnalyzeRequest(code=code, language="python")
    ).model_dump(by_alias=True)
    finding = next(
        item for item in analysis["findings"] if item["type"] == finding_type
    )
    return fix_service.apply_fix(
        ApplyFixRequest(code=code, findingId=finding["id"])
    ).model_dump(by_alias=True)


def test_analyze_includes_flat_code_action_for_supported_finding() -> None:
    response = analysis_service.analyze(
        AnalyzeRequest(code="print(x)\n", language="python")
    ).model_dump(by_alias=True)

    action = response["findings"][0]["codeAction"]

    assert action["title"] == "Create variable 'x'"
    assert action["replacement"] == "x = None\n"
    assert action["startLine"] == 1
    assert "range" not in action


def test_apply_fix_creates_undefined_variable() -> None:
    response = apply_first_fix("print(x)\n", "undefined_variable")

    assert response == {
        "applied": True,
        "updatedCode": "x = None\nprint(x)\n",
        "message": "Applied fix successfully",
    }


def test_apply_fix_corrects_infinite_loop_increment() -> None:
    response = apply_first_fix(
        "x = 10\nwhile x > 0:\n    x += 1\n",
        "infinite_loop_risk",
    )

    assert response["applied"] is True
    assert response["updatedCode"] == "x = 10\nwhile x > 0:\n    x -= 1\n"


def test_apply_fix_corrects_infinite_loop_decrement() -> None:
    response = apply_first_fix(
        "x = 0\nwhile x < 10:\n    x -= 1\n",
        "infinite_loop_risk",
    )

    assert response["applied"] is True
    assert response["updatedCode"] == "x = 0\nwhile x < 10:\n    x += 1\n"


def test_apply_fix_adds_missing_base_case() -> None:
    response = apply_first_fix(
        "def recurse(n):\n    recurse(n-1)\n",
        "missing_base_case",
    )

    assert response["applied"] is True
    assert response["updatedCode"] == (
        "def recurse(n):\n"
        "    if n <= 0:\n"
        "        return\n"
        "    recurse(n-1)\n"
    )


def test_apply_fix_corrects_binary_search_high_boundary() -> None:
    response = apply_first_fix(
        "if arr[mid] < target:\n"
        "    high = mid - 1\n",
        "binary_search_logic_issue",
    )

    assert response["applied"] is True
    assert response["updatedCode"] == "if arr[mid] < target:\n    low = mid + 1\n"


def test_apply_fix_corrects_binary_search_low_boundary() -> None:
    response = apply_first_fix(
        "if arr[mid] > target:\n"
        "    low = mid + 1\n",
        "binary_search_logic_issue",
    )

    assert response["applied"] is True
    assert response["updatedCode"] == "if arr[mid] > target:\n    high = mid - 1\n"


def test_apply_fix_removes_dead_code_statement() -> None:
    response = apply_first_fix(
        "def f(x):\n"
        "    return x\n"
        "    print(x)\n",
        "dead_code",
    )

    assert response["applied"] is True
    assert response["updatedCode"] == "def f(x):\n    return x\n"


def test_apply_fix_removes_unreachable_false_branch() -> None:
    response = apply_first_fix(
        "if False:\n"
        "    print('hello')\n",
        "unreachable_code",
    )

    assert response["applied"] is True
    assert response["updatedCode"] == ""


def test_apply_fix_returns_false_for_stale_or_unsupported_finding() -> None:
    response = fix_service.apply_fix(
        ApplyFixRequest(code="x = 1\n", findingId="finding_001")
    ).model_dump(by_alias=True)

    assert response == {
        "applied": False,
        "updatedCode": "x = 1\n",
        "message": "No automatic fix available",
    }
