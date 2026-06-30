from app.rules.base import BaseRule
from app.rules.models import RuleFinding
from app.semantic.models import ConditionalInfo, SemanticRepresentation


class BinarySearchRule(BaseRule):
    rule_id = "BIN_SEARCH_001"
    finding_type = "binary_search_logic_issue"
    severity = "high"
    message = "Binary search branch updates the wrong boundary for the comparison."

    def check(self, semantic: SemanticRepresentation) -> list[RuleFinding]:
        findings: list[RuleFinding] = []
        assignments_by_line = {assignment.line: assignment for assignment in semantic.assignments}

        for conditional in semantic.conditionals:
            next_assignment = assignments_by_line.get(conditional.line + 1)
            if next_assignment is None:
                continue
            if self._is_wrong_high_update(conditional, next_assignment.target):
                findings.append(self.finding(line=next_assignment.line))
            elif self._is_wrong_low_update(conditional, next_assignment.target):
                findings.append(self.finding(line=next_assignment.line))

        return findings

    def _is_wrong_high_update(self, conditional: ConditionalInfo, target: str) -> bool:
        return (
            conditional.comparison_operator == "Lt"
            and bool(conditional.left_variables)
            and bool(conditional.right_variables)
            and target == "high"
        )

    def _is_wrong_low_update(self, conditional: ConditionalInfo, target: str) -> bool:
        return (
            conditional.comparison_operator == "Gt"
            and bool(conditional.left_variables)
            and bool(conditional.right_variables)
            and target == "low"
        )
