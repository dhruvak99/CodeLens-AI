from abc import ABC, abstractmethod
from typing import cast

from app.schemas.common import FindingType, Severity
from app.rules.models import RuleFinding
from app.rules.registry import RuleRegistry
from app.semantic.models import SemanticRepresentation


class BaseRule(ABC):
    rule_id: str
    finding_type: str
    severity: str
    message: str

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if not getattr(cls, "abstract", False):
            RuleRegistry.register(cls)

    @abstractmethod
    def check(self, semantic: SemanticRepresentation) -> list[RuleFinding]:
        raise NotImplementedError

    def finding(self, *, line: int, column: int = 1, message: str | None = None) -> RuleFinding:
        return RuleFinding(
            id="finding_pending",
            type=cast(FindingType, self.finding_type),
            severity=cast(Severity, self.severity),
            message=message or self.message,
            line=line,
            column=column,
            rule=self.rule_id,
            codeAction=None,
        )
