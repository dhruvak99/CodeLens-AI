from app.rules.base import BaseRule
from app.rules.engine import RuleEngine
from app.rules.registry import RuleRegistry

# Import rule modules so subclasses register themselves.
from app.rules import (  # noqa: F401
    binary_search,
    dead_code,
    infinite_loop,
    recursion,
    undefined_variable,
    unreachable_code,
    unused_variable,
)

__all__ = ["BaseRule", "RuleEngine", "RuleRegistry"]
