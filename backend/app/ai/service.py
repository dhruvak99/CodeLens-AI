import json
import logging
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, cast

from app.ai.models import ExplanationContext
from app.ai.prompt_builder import PromptBuilder
from app.ai.response_parser import ResponseParser
from app.schemas.explain import ExplainResponse


LOCAL_OLLAMA_HOSTS = {"localhost", "127.0.0.1", "::1"}
logger = logging.getLogger(__name__)


class AIExplanationService:
    def __init__(
        self,
        prompt_builder: PromptBuilder | None = None,
        response_parser: ResponseParser | None = None,
    ) -> None:
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.response_parser = response_parser or ResponseParser()

    def explain(self, context: ExplanationContext) -> ExplainResponse:
        url = os.environ.get("OLLAMA_URL")
        model = os.environ.get("OLLAMA_MODEL")
        if not url or not model:
            logger.warning(
                "AI explanation unavailable: missing OLLAMA_URL or OLLAMA_MODEL."
            )
            return self.response_parser.unavailable()

        if not self._is_local_url(url):
            logger.warning(
                "AI explanation unavailable: OLLAMA_URL must point to localhost. "
                "Received %s",
                url,
            )
            return self.response_parser.unavailable()

        prompt = self.prompt_builder.build(context)
        try:
            content = self._generate(url=url, model=model, prompt=prompt)
            return self.response_parser.parse(content)
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            logger.error(
                "AI explanation unavailable: Ollama HTTP %s from %s. Body: %s",
                exc.code,
                exc.url,
                body,
            )
        except (
            OSError,
            TimeoutError,
            urllib.error.URLError,
            ValueError,
            json.JSONDecodeError,
        ) as exc:
            logger.exception("AI explanation unavailable: %s", exc)
        return self.response_parser.unavailable()

    def _generate(self, url: str, model: str, prompt: str) -> str:
        endpoint = f"{url.rstrip('/')}/api/generate"
        body = json.dumps(
            {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "think": False,
                "options": {
                    "temperature": 0.2,
                    "num_predict": 500,
                },
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            endpoint,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))

        if not isinstance(payload, dict):
            raise ValueError("Ollama response did not include text.")
        payload_dict = cast(dict[str, Any], payload)
        response_text = payload_dict.get("response")
        if response_text == "" and isinstance(payload_dict.get("thinking"), str):
            response_text = payload_dict.get("thinking")
        if not isinstance(response_text, str):
            raise ValueError("Ollama response did not include text.")
        return response_text

    def _is_local_url(self, url: str) -> bool:
        parsed = urllib.parse.urlparse(url)
        return parsed.scheme in {"http", "https"} and parsed.hostname in LOCAL_OLLAMA_HOSTS
