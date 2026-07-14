import logging
from dataclasses import dataclass

import requests
from requests import RequestException

from app.services.llm_sql_generation_service import OLLAMA_GENERATE_URL

logger = logging.getLogger(__name__)

SQL_TUTOR_MODEL = "qwen2.5:7b"


class SQLTutorError(Exception):
    pass


@dataclass(frozen=True)
class SQLTutorContext:
    question: str
    generated_sql: str
    selected_table: str | None
    table_schema: list[str]
    result_preview: list[dict[str, str | int | float | bool | None]]
    validation_status: str


def explain_sql(context: SQLTutorContext) -> str:
    prompt = build_sql_tutor_prompt(context)
    try:
        response = requests.post(
            OLLAMA_GENERATE_URL,
            json={
                "model": SQL_TUTOR_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()
    except RequestException as error:
        logger.exception("SQL tutor explanation request failed")
        raise SQLTutorError("SQL tutor explanation request failed.") from error

    payload = response.json()
    explanation = str(payload.get("response", "")).strip()
    if not explanation:
        raise SQLTutorError("SQL tutor returned an empty explanation.")
    return explanation


def build_sql_tutor_prompt(context: SQLTutorContext) -> str:
    schema_lines = "\n".join(f"- {column}" for column in context.table_schema) or "- No schema provided"
    result_preview = context.result_preview[:5]

    return (
        "You are an expert SQL tutor.\n\n"
        "The SQL query has ALREADY been generated.\n\n"
        "Do NOT generate another SQL query.\n"
        "Do NOT modify the SQL.\n"
        "Explain ONLY the provided SQL.\n\n"
        "Structure your response using Markdown.\n\n"
        "Include:\n\n"
        "## Summary\n\n"
        "Briefly explain what the query does.\n\n"
        "## Clause Breakdown\n\n"
        "Explain every SQL clause used.\n\n"
        "## SQL Concepts\n\n"
        "List concepts such as SELECT, WHERE, GROUP BY, ORDER BY, Aggregate Function, JOIN, Subquery, LIMIT.\n"
        "Only include concepts actually used.\n\n"
        "## Difficulty\n\n"
        "Choose exactly one: Beginner, Intermediate, Advanced.\n\n"
        "## Alternative Solution\n\n"
        "If another SQL solution exists, show it. Otherwise say: 'The current solution is already appropriate.'\n\n"
        "## Tutor Tip\n\n"
        "Give one useful learning tip related to the query.\n\n"
        "Keep the explanation educational, accurate, beginner-friendly, and under 250 words.\n"
        "Do not invent tables.\n"
        "Do not invent columns.\n"
        "Do not regenerate SQL.\n\n"
        "Structured context:\n"
        f"Question: {context.question}\n"
        f"Selected table: {context.selected_table or 'Not provided'}\n"
        f"Validation status: {context.validation_status}\n\n"
        "Table schema:\n"
        f"{schema_lines}\n\n"
        "Generated SQL:\n"
        f"{context.generated_sql}\n\n"
        "Result preview:\n"
        f"{result_preview}\n"
    )
