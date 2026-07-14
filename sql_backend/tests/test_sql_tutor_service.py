import unittest
from unittest.mock import Mock, patch

from app.services.sql_tutor_service import (
    SQL_TUTOR_MODEL,
    SQLTutorContext,
    build_sql_tutor_prompt,
    explain_sql,
)


class SQLTutorServiceTests(unittest.TestCase):
    def test_prompt_instructs_tutor_not_to_generate_sql(self) -> None:
        prompt = build_sql_tutor_prompt(
            SQLTutorContext(
                question="Show the course with highest credits",
                generated_sql="SELECT * FROM courses ORDER BY credits DESC LIMIT 1;",
                selected_table="courses",
                table_schema=["course_id INTEGER", "course_name TEXT", "credits INTEGER"],
                result_preview=[{"course_name": "Artificial Intelligence", "credits": 5}],
                validation_status="valid",
            )
        )

        self.assertIn("Do NOT generate another SQL query.", prompt)
        self.assertIn("Explain ONLY the provided SQL.", prompt)
        self.assertEqual(SQL_TUTOR_MODEL, "qwen2.5:7b")
        self.assertIn("courses", prompt)
        self.assertIn("credits INTEGER", prompt)
        self.assertIn("SELECT * FROM courses ORDER BY credits DESC LIMIT 1;", prompt)

    def test_explain_sql_uses_qwen_tutor_model(self) -> None:
        mock_response = Mock()
        mock_response.json.return_value = {"response": "## Summary\nThis query lists courses."}
        mock_response.raise_for_status.return_value = None

        with patch("app.services.sql_tutor_service.requests.post", return_value=mock_response) as post:
            explanation = explain_sql(
                SQLTutorContext(
                    question="Show courses",
                    generated_sql="SELECT * FROM courses;",
                    selected_table="courses",
                    table_schema=["course_id INTEGER"],
                    result_preview=[],
                    validation_status="valid",
                )
            )

        self.assertEqual(explanation, "## Summary\nThis query lists courses.")
        self.assertEqual(post.call_args.kwargs["json"]["model"], "qwen2.5:7b")
        self.assertFalse(post.call_args.kwargs["json"]["stream"])


if __name__ == "__main__":
    unittest.main()
