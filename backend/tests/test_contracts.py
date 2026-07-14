from app.schemas.analysis import AnalyzeRequest
from app.schemas.explain import ExplainRequest
from app.schemas.fix import ApplyFixRequest
from app.schemas.metrics import MetricsRequest
from app.schemas.runtime import RuntimeRequest
from app.services.analysis_service import analysis_service
from app.services.explain_service import explain_service
from app.services.fix_service import fix_service
from app.services.metrics_service import metrics_service
from app.services.runtime_service import runtime_service


def test_analyze_contract_uses_camel_case_response_fields() -> None:
    response = analysis_service.analyze(
        AnalyzeRequest(
            code=(
                "def binary_search(arr, target):\n"
                "    low = 0\n"
                "    while low < target:\n"
                "        low += 1\n"
            ),
            language="python",
        )
    ).model_dump(by_alias=True)

    assert response["runtimeAvailable"] is False
    assert response["findings"] == []
    assert response["errors"] == []
    assert any(
        node["type"] == "function" and node["label"] == "binary_search"
        for node in response["semanticGraph"]["nodes"]
    )
    assert any(edge["label"] == "modifies" for edge in response["semanticGraph"]["edges"])
    assert response["metrics"]["timeComplexity"] == "O(n)"


def test_analyze_contract_returns_structured_syntax_errors() -> None:
    response = analysis_service.analyze(
        AnalyzeRequest(code="def broken(:\n    x = 1", language="python")
    ).model_dump(by_alias=True)

    assert response["findings"] == []
    assert response["errors"][0]["type"] == "syntax_error"
    assert response["semanticGraph"] == {"nodes": [], "edges": []}


def test_explain_contract() -> None:
    response = explain_service.explain(
        ExplainRequest(code="x = 1", findingId="finding_001")
    ).model_dump(by_alias=True)

    assert response["summary"] == "AI explanation unavailable."
    assert response["explanation"] == "AI explanation unavailable."
    assert response["unavailable"] is True
    assert response["confidence"] == 0.0


def test_apply_fix_contract_does_not_change_code_yet() -> None:
    response = fix_service.apply_fix(
        ApplyFixRequest(code="x = 1", findingId="finding_001")
    ).model_dump(by_alias=True)

    assert response == {
        "updatedCode": "x = 1",
        "applied": False,
        "message": "No automatic fix available",
    }


def test_runtime_contract() -> None:
    response = runtime_service.get_runtime_trace(
        RuntimeRequest(code="x = 1")
    ).model_dump(by_alias=True)

    assert response["success"] is True
    assert response["steps"][0]["stepNumber"] == 1
    assert response["steps"][0]["variables"] == {"x": "1"}
    assert response["output"] == []
    assert response["error"] is None


def test_metrics_contract() -> None:
    response = metrics_service.calculate_metrics(
        MetricsRequest(code="x = 1")
    ).model_dump(by_alias=True)

    assert response["timeComplexity"] == "O(1)"
    assert response["spaceComplexity"] == "O(1)"
    assert response["cyclomaticComplexity"] == 1
    assert response["maintainabilityScore"] <= 10
