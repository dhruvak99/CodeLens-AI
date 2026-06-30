from app.rules.base import BaseRule
from app.rules.models import RuleFinding
from app.semantic.models import SemanticRepresentation


class MissingBaseCaseRule(BaseRule):
    rule_id = "RECURSION_001"
    finding_type = "missing_base_case"
    severity = "high"
    message = "Recursive function has no obvious conditional base case."

    def check(self, semantic: SemanticRepresentation) -> list[RuleFinding]:
        findings: list[RuleFinding] = []
        conditional_scopes = {conditional.scope for conditional in semantic.conditionals}

        for candidate in semantic.recursion_candidates:
            if candidate.scope not in conditional_scopes:
                findings.append(self.finding(line=candidate.line))

        return findings
