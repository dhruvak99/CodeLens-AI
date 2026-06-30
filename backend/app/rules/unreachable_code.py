from app.rules.base import BaseRule
from app.rules.models import RuleFinding
from app.semantic.models import SemanticRepresentation


class UnreachableCodeRule(BaseRule):
    rule_id = "UNREACHABLE_001"
    finding_type = "unreachable_code"
    severity = "medium"
    message = "Branch is unreachable because its condition is constant."

    def check(self, semantic: SemanticRepresentation) -> list[RuleFinding]:
        return [
            self.finding(line=item.line, message=f"Unreachable branch: {item.reason}.")
            for item in semantic.unreachable_branches
        ]
