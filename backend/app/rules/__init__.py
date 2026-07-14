from app.rules.base import BaseRule
from app.rules.engine import RuleEngine
from app.rules.registry import RuleRegistry

# Import rule modules so subclasses register themselves.
from app.rules import (  # noqa: F401
    binary_search,
    dangerous_import,
    dead_code,
    infinite_loop,
    missing_return,
    recursion,
    shadowed_variable,
    undefined_variable,
    unreachable_code,
    unused_variable,
)

__all__ = ["BaseRule", "RuleEngine", "RuleRegistry"]
