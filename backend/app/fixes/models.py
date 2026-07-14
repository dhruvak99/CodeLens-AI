from dataclasses import dataclass

from app.schemas.common import CodeAction, Finding


@dataclass(frozen=True)
class FixContext:
    code: str
    finding: Finding


@dataclass(frozen=True)
class FixResult:
    applied: bool
    updated_code: str
    message: str


FixAction = CodeAction
