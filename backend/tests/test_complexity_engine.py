from app.schemas.analysis import AnalyzeRequest
from app.schemas.metrics import MetricsRequest
from app.services.analysis_service import analysis_service
from app.services.metrics_service import metrics_service
from typing import cast


def metric_for(code: str, key: str) -> str | int | float:
    response = analysis_service.analyze(
        AnalyzeRequest(code=code, language="python")
    ).model_dump(by_alias=True)
    return cast(str | int | float, response["metrics"][key])


def test_constant_time_for_assignment() -> None:
    assert metric_for("x = 10", "timeComplexity") == "O(1)"
    assert metric_for("x = 10", "spaceComplexity") == "O(1)"
    assert metric_for("x = 10", "cyclomaticComplexity") == 1


def test_single_loop_is_linear() -> None:
    code = "for i in range(n):\n    print(i)\n"

    assert metric_for(code, "timeComplexity") == "O(n)"
    assert metric_for(code, "loops") == 1


def test_nested_loops_are_quadratic() -> None:
    code = "for i in range(n):\n    for j in range(n):\n        print(i, j)\n"

    assert metric_for(code, "timeComplexity") == "O(n²)"
    assert metric_for(code, "loops") == 2


def test_binary_search_pattern_is_logarithmic() -> None:
    code = (
        "def binary_search(arr, target):\n"
        "    low = 0\n"
        "    high = len(arr)-1\n"
        "\n"
        "    while low <= high:\n"
        "        mid = (low + high) // 2\n"
        "\n"
        "        if arr[mid] == target:\n"
        "            return mid\n"
        "        elif arr[mid] < target:\n"
        "            low = mid + 1\n"
        "        else:\n"
        "            high = mid - 1\n"
    )

    assert metric_for(code, "timeComplexity") == "O(log n)"


def test_fibonacci_recursion_is_exponential() -> None:
    code = (
        "def fib(n):\n"
        "    if n <= 1:\n"
        "        return n\n"
        "    return fib(n-1) + fib(n-2)\n"
    )

    assert metric_for(code, "timeComplexity") == "O(2ⁿ)"
    assert metric_for(code, "spaceComplexity") == "O(n)"


def test_list_comprehension_is_linear_and_nested_comprehension_is_quadratic() -> None:
    assert metric_for("values = [x for x in range(n)]", "timeComplexity") == "O(n)"
    assert (
        metric_for(
            "pairs = [(x, y) for x in range(n) for y in range(n)]",
            "timeComplexity",
        )
        == "O(n²)"
    )


def test_cyclomatic_complexity_counts_decision_points() -> None:
    code = (
        "try:\n"
        "    if a and b or c:\n"
        "        pass\n"
        "except Exception:\n"
        "    pass\n"
    )

    assert metric_for(code, "cyclomaticComplexity") == 5


def test_metrics_endpoint_uses_real_engine() -> None:
    response = metrics_service.calculate_metrics(
        MetricsRequest(code="for i in range(n):\n    print(i)\n")
    ).model_dump(by_alias=True)

    assert response["timeComplexity"] == "O(n)"
    assert response["loops"] == 1
