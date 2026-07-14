import json
import logging
from urllib.error import URLError
from unittest.mock import patch

import pytest
from pytest import MonkeyPatch

from app.ai.models import ExplanationContext
from app.ai.prompt_builder import PromptBuilder
from app.ai.response_parser import ResponseParser
from app.ai.service import AIExplanationService
from app.schemas.common import Finding, Metrics
from app.semantic.errors import AnalysisError


def test_prompt_builder_uses_existing_finding_and_metrics_only() -> None:
    prompt = PromptBuilder().build(
        ExplanationContext(
            code="print(x)\n",
            finding_id="finding_001",
            finding=Finding(
                id="finding_001",
                type="undefined_variable",
                severity="high",
                message="Variable 'x' is not defined.",
                line=1,
                column=7,
                rule="UNDEF_VAR_001",
            ),
            metrics=Metrics(
                timeComplexity="O(1)",
                spaceComplexity="O(1)",
                cyclomaticComplexity=1,
                functions=0,
                loops=0,
                linesOfCode=1,
                maintainabilityScore=9.5,
            ),
        )
    )

    assert "The deterministic analyzer is the source of truth." in prompt
    assert "Do not detect new bugs." in prompt
    assert "Undefined Variable" in prompt
    assert "Variable 'x' is not defined." in prompt
    assert "Time Complexity: O(1)" in prompt
    assert "print(x)" in prompt


def test_prompt_builder_supports_syntax_error() -> None:
    prompt = PromptBuilder().build(
        ExplanationContext(
            code="while:\n",
            finding_id="syntax-0",
            error=AnalysisError(
                type="syntax_error",
                message="invalid syntax",
                line=1,
                column=6,
            ),
        )
    )

    assert "Syntax Error" in prompt
    assert "invalid syntax" in prompt
    assert "while:" in prompt


def test_response_parser_returns_structured_json() -> None:
    response = ResponseParser().parse(
        json.dumps(
            {
                "summary": "Undefined variable.",
                "rootCause": "The name was read before assignment.",
                "explanation": "Python resolves names at runtime.",
                "howToFix": "Define the variable first.",
                "correctedExample": "x = None\nprint(x)",
                "learningTip": "Read before write causes NameError.",
                "bestPractice": "Initialize values near first use.",
                "confidence": 0.97,
            }
        )
    )

    assert response.summary == "Undefined variable."
    assert response.root_cause == "The name was read before assignment."
    assert response.confidence == 0.97
    assert response.unavailable is False


def test_ai_service_returns_unavailable_without_ollama_config(
    caplog: pytest.LogCaptureFixture,
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.delenv("OLLAMA_URL", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)

    caplog.set_level(logging.WARNING, logger="app.ai.service")
    response = AIExplanationService().explain(
        ExplanationContext(code="print(x)\n", finding_id="finding_001")
    )

    assert response.unavailable is True
    assert response.summary == "AI explanation unavailable."
    assert "missing OLLAMA_URL or OLLAMA_MODEL" in caplog.text


def test_ai_service_rejects_non_local_ollama_url(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("OLLAMA_URL", "https://example.com")
    monkeypatch.setenv("OLLAMA_MODEL", "qwen3:4b")

    response = AIExplanationService().explain(
        ExplanationContext(code="print(x)\n", finding_id="finding_001")
    )

    assert response.unavailable is True


def test_ai_service_handles_ollama_connection_failure(
    monkeypatch: MonkeyPatch,
) -> None:
    class FailingAIExplanationService(AIExplanationService):
        def _generate(self, url: str, model: str, prompt: str) -> str:
            raise URLError("offline")

    monkeypatch.setenv("OLLAMA_URL", "http://localhost:11434")
    monkeypatch.setenv("OLLAMA_MODEL", "qwen3:4b")

    response = FailingAIExplanationService().explain(
        ExplanationContext(code="print(x)\n", finding_id="finding_001")
    )

    assert response.unavailable is True


def test_ai_service_accepts_qwen_thinking_fallback() -> None:
    class FakeHTTPResponse:
        def __enter__(self) -> "FakeHTTPResponse":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(
                {
                    "response": "",
                    "thinking": json.dumps(
                        {
                            "summary": "ok",
                            "rootCause": "ok",
                            "explanation": "ok",
                            "howToFix": "ok",
                            "correctedExample": "ok",
                            "learningTip": "ok",
                            "bestPractice": "ok",
                            "confidence": 0.9,
                        }
                    ),
                }
            ).encode("utf-8")

    with patch("urllib.request.urlopen", return_value=FakeHTTPResponse()):
        content = AIExplanationService()._generate(
            url="http://localhost:11434",
            model="qwen3:4b",
            prompt="Return JSON.",
        )

    assert json.loads(content)["summary"] == "ok"
