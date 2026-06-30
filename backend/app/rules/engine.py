from app.rules.models import RuleFinding
from app.rules.registry import RuleRegistry
from app.semantic.models import SemanticRepresentation


class RuleEngine:
    def run(self, semantic: SemanticRepresentation) -> list[RuleFinding]:
        findings: list[RuleFinding] = []

        for rule_class in RuleRegistry.rules():
            try:
                findings.extend(rule_class().check(semantic))
            except Exception:
                continue

        sorted_findings = sorted(findings, key=lambda finding: (finding.line, finding.column, finding.rule))

        return [
            finding.model_copy(update={"id": f"finding_{index:03d}"})
            for index, finding in enumerate(sorted_findings, start=1)
        ]
