from app.rules.base import BaseRule
from app.rules.models import RuleFinding
from app.semantic.models import SemanticRepresentation


class MissingReturnRule(BaseRule):
    rule_id = "MISSING_RETURN_001"
    finding_type = "missing_return"
    severity = "medium"
    message = "Function has an execution path that can reach the end without returning a value."

    def check(self, semantic: SemanticRepresentation) -> list[RuleFinding]:
        findings: list[RuleFinding] = []

        for function in semantic.functions:
            if function.name == "__init__":
                continue

            scope = f"{function.scope}.{function.name}"
            return_lines = [
                event.line
                for event in semantic.control_flow_events
                if event.scope == scope and event.type == "return"
            ]
            if not return_lines:
                continue

            branch_lines = [
                conditional.line
                for conditional in semantic.conditionals
                if conditional.scope == scope
            ]
            branch_lines.extend(
                loop.line for loop in semantic.loops if loop.scope == scope
            )
            if not branch_lines:
                continue

            only_return_is_branch_body = len(return_lines) == 1 and any(
                return_lines[0] == branch_line + 1 for branch_line in branch_lines
            )
            no_final_return_after_branching = max(return_lines) <= max(branch_lines)

            if only_return_is_branch_body or no_final_return_after_branching:
                findings.append(
                    self.finding(
                        line=function.line,
                        column=function.column,
                        message=(
                            f"Function '{function.name}' may finish without "
                            "returning a value."
                        ),
                    )
                )

        return findings
