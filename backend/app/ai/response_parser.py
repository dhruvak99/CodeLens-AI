import json
from typing import Any

from app.schemas.explain import ExplainResponse


class ResponseParser:
    def parse(self, content: str) -> ExplainResponse:
        payload = self._load_json(content)
        return ExplainResponse(
            summary=str(payload.get("summary", "")).strip(),
            rootCause=str(payload.get("rootCause", "")).strip(),
            explanation=str(payload.get("explanation", "")).strip(),
            howToFix=str(payload.get("howToFix", "")).strip(),
            correctedExample=str(payload.get("correctedExample", "")).strip(),
            learningTip=str(payload.get("learningTip", "")).strip(),
            bestPractice=str(payload.get("bestPractice", "")).strip(),
            confidence=self._confidence(payload.get("confidence")),
            unavailable=False,
        )

    def unavailable(self) -> ExplainResponse:
        return ExplainResponse(
            summary="AI explanation unavailable.",
            rootCause="AI explanation unavailable.",
            explanation="AI explanation unavailable.",
            howToFix="AI explanation unavailable.",
            correctedExample="",
            learningTip="AI explanation unavailable.",
            bestPractice="AI explanation unavailable.",
            confidence=0.0,
            unavailable=True,
        )

    def _load_json(self, content: str) -> dict[str, Any]:
        stripped = content.strip()
        if stripped.startswith("```"):
            stripped = stripped.removeprefix("```json").removeprefix("```").strip()
            stripped = stripped.removesuffix("```").strip()

        data = json.loads(stripped)
        if not isinstance(data, dict):
            raise ValueError("Ollama response was not a JSON object.")
        return data

    def _confidence(self, value: object) -> float:
        if isinstance(value, int | float):
            return max(0.0, min(float(value), 1.0))
        return 0.0

