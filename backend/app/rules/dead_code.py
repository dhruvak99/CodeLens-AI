from app.rules.base import BaseRule
from app.rules.models import RuleFinding
from app.semantic.models import SemanticRepresentation


class DeadCodeRule(BaseRule):
    rule_id = "DEAD_CODE_001"
    finding_type = "dead_code"
    severity = "medium"
    message = "Statement appears after a terminal control-flow statement."

    def check(self, semantic: SemanticRepresentation) -> list[RuleFinding]:
        return [
            self.finding(
                line=item.line,
                message=f"Statement is dead code after {item.after}.",
            )
            for item in semantic.dead_code
        ]
