from app.rules.base import BaseRule
from app.rules.models import RuleFinding
from app.semantic.models import LoopInfo, SemanticRepresentation, VariableUpdateInfo


class InfiniteLoopRule(BaseRule):
    rule_id = "INF_LOOP_001"
    finding_type = "infinite_loop_risk"
    severity = "high"
    message = "Loop update appears to move a condition variable away from termination."

    def check(self, semantic: SemanticRepresentation) -> list[RuleFinding]:
        findings: list[RuleFinding] = []
        for loop in semantic.loops:
            if loop.type != "while":
                continue
            for update in loop.variable_updates:
                if update.name not in loop.condition_variables:
                    continue
                if self._moves_away(loop, update):
                    findings.append(self.finding(line=update.line))
        return findings

    def _moves_away(self, loop: LoopInfo, update: VariableUpdateInfo) -> bool:
        operator = loop.comparison_operator
        if operator is None:
            return False

        if update.name in loop.left_variables:
            return (
                operator in {"Gt", "GtE"} and update.direction == "increase"
            ) or (operator in {"Lt", "LtE"} and update.direction == "decrease")

        if update.name in loop.right_variables:
            return (
                operator in {"Gt", "GtE"} and update.direction == "decrease"
            ) or (operator in {"Lt", "LtE"} and update.direction == "increase")

        return False
