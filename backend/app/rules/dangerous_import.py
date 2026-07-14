from app.rules.base import BaseRule
from app.rules.models import RuleFinding
from app.semantic.models import SemanticRepresentation


DANGEROUS_MODULES = {
    "ctypes",
    "multiprocessing",
    "os",
    "pickle",
    "shutil",
    "signal",
    "socket",
    "subprocess",
}


class DangerousImportRule(BaseRule):
    rule_id = "DANGEROUS_IMPORT_001"
    finding_type = "dangerous_import"
    severity = "high"
    message = "Program imports a module that can perform unsafe system operations."

    def check(self, semantic: SemanticRepresentation) -> list[RuleFinding]:
        findings: list[RuleFinding] = []
        seen: set[tuple[str, int]] = set()

        for import_info in semantic.imports:
            root_module = import_info.name.split(".", maxsplit=1)[0]
            if root_module not in DANGEROUS_MODULES:
                continue

            key = (root_module, import_info.line)
            if key in seen:
                continue
            seen.add(key)
            findings.append(
                self.finding(
                    line=import_info.line,
                    message=f"Import '{import_info.name}' uses dangerous module '{root_module}'.",
                )
            )

        return findings

