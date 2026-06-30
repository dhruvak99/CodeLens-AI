import time
import tracemalloc

from app.schemas.analysis import AnalyzeRequest
from app.services.analysis_service import analysis_service


def test_large_and_deep_inputs_stay_demo_safe() -> None:
    cases = [
        "\n".join(f"value_{index} = {index}" for index in range(1200)),
        "\n".join(
            [
                f"def function_{index}(x):\n"
                "    if x > 0:\n"
                "        return x\n"
                "    return 0"
                for index in range(200)
            ]
        ),
        "\n".join(
            [
                f"class Class_{index}:\n"
                "    def method(self, value):\n"
                "        return value"
                for index in range(150)
            ]
        ),
        "\n".join("    " * depth + "if True:" for depth in range(95))
        + "\n"
        + "    " * 95
        + "value = 1\n",
    ]

    timings: list[float] = []
    tracemalloc.start()
    try:
        for code in cases:
            start = time.perf_counter()
            response = analysis_service.analyze(
                AnalyzeRequest(code=code, language="python")
            )
            timings.append((time.perf_counter() - start) * 1000)
            assert isinstance(response.findings, list)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    assert sum(timings) / len(timings) < 500
    assert max(timings) < 1500
    assert peak < 64 * 1024 * 1024
