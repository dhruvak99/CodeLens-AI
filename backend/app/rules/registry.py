from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.rules.base import BaseRule


class RuleRegistry:
    _rules: list[type["BaseRule"]] = []

    @classmethod
    def register(cls, rule: type["BaseRule"]) -> None:
        if rule not in cls._rules:
            cls._rules.append(rule)

    @classmethod
    def rules(cls) -> list[type["BaseRule"]]:
        return list(cls._rules)
