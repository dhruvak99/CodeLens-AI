from app.ai.models import ExplanationContext


SUPPORTED_FINDING_LABELS = {
    "binary_search_logic_issue": "Binary Search Logic Issue",
    "dead_code": "Dead Code",
    "infinite_loop_risk": "Infinite Loop Risk",
    "missing_base_case": "Missing Base Case",
    "syntax_error": "Syntax Error",
    "undefined_variable": "Undefined Variable",
    "unreachable_code": "Unreachable Code",
    "unused_variable": "Unused Variable",
}


class PromptBuilder:
    def build(self, context: ExplanationContext) -> str:
        finding_type = self._finding_type(context)
        message = self._message(context)
        relevant_code = self._relevant_code(context)
        metrics = self._metrics(context)
        runtime = self._runtime_summary(context)

        return (
            "You are CodeLens AI's explanation layer. Behave like a concise "
            "programming tutor.\n\n"
            "Rules:\n"
            "- The deterministic analyzer is the source of truth.\n"
            "- Do not detect new bugs.\n"
            "- Do not calculate new complexity.\n"
            "- Do not decide or invent code fixes.\n"
            "- Explain only the supplied finding, metric, and runtime facts.\n"
            "- Maximum 250 words.\n"
            "- Return valid JSON only.\n\n"
            f"Finding Type:\n{finding_type}\n\n"
            f"Message:\n{message}\n\n"
            f"Relevant Code:\n```python\n{relevant_code}\n```\n\n"
            f"Complexity Metrics:\n{metrics}\n\n"
            f"Runtime Summary:\n{runtime}\n\n"
            "Return JSON with exactly these fields:\n"
            "{\n"
            '  "summary": "short issue summary",\n'
            '  "rootCause": "why this happened",\n'
            '  "explanation": "how Python or the algorithm behaves",\n'
            '  "howToFix": "how to address the existing analyzer finding",\n'
            '  "correctedExample": "minimal corrected code example",\n'
            '  "learningTip": "one learning tip",\n'
            '  "bestPractice": "one best practice",\n'
            '  "confidence": 0.0\n'
            "}"
        )

    def _finding_type(self, context: ExplanationContext) -> str:
        if context.error:
            return SUPPORTED_FINDING_LABELS.get(context.error.type, "Syntax Error")
        if context.finding:
            return SUPPORTED_FINDING_LABELS.get(
                context.finding.type, self._title_case(context.finding.type)
            )
        return f"Finding ID {context.finding_id}"

    def _message(self, context: ExplanationContext) -> str:
        if context.error:
            return context.error.message
        if context.finding:
            return context.finding.message
        return "Explain the selected analyzer result."

    def _relevant_code(self, context: ExplanationContext) -> str:
        line_number = context.error.line if context.error else None
        if context.finding:
            line_number = context.finding.line

        lines = context.code.splitlines()
        if not lines:
            return context.code

        if line_number is None:
            return "\n".join(lines[:40])

        index = max(line_number - 1, 0)
        start = max(index - 3, 0)
        end = min(index + 4, len(lines))
        return "\n".join(lines[start:end])

    def _metrics(self, context: ExplanationContext) -> str:
        metrics = context.metrics
        if not metrics:
            return "Unavailable."

        return (
            f"Time Complexity: {metrics.time_complexity}\n"
            f"Space Complexity: {metrics.space_complexity}\n"
            f"Cyclomatic Complexity: {metrics.cyclomatic_complexity}\n"
            f"Functions: {metrics.functions}\n"
            f"Loops: {metrics.loops}\n"
            f"Lines of Code: {metrics.lines_of_code}\n"
            f"Maintainability Score: {metrics.maintainability_score}"
        )

    def _runtime_summary(self, context: ExplanationContext) -> str:
        summary = context.runtime_summary
        if not summary:
            return "Unavailable."

        output = ", ".join(summary.output or []) or "No output captured."
        variables = summary.final_variables or {}
        variables_text = (
            ", ".join(f"{name}={value}" for name, value in variables.items())
            if variables
            else "No final variables captured."
        )
        return (
            f"Steps: {summary.steps}\n"
            f"Output: {output}\n"
            f"Final Variables: {variables_text}\n"
            "Explain runtime flow in at most 100 words if useful."
        )

    def _title_case(self, value: str) -> str:
        return " ".join(part.capitalize() for part in value.split("_"))

