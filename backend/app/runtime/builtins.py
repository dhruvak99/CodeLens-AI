import ast
from collections.abc import Sequence
from typing import Any

from app.runtime.models import RuntimeErrorType, RuntimeFault


DISALLOWED_CALLS = {
    "eval",
    "exec",
    "globals",
    "locals",
    "open",
    "subprocess",
    "threading",
    "multiprocessing",
}


def build_range(args: Sequence[Any], node: ast.AST) -> range:
    if len(args) not in {1, 2, 3}:
        raise RuntimeFault(
            RuntimeErrorType.TYPE_MISMATCH,
            "range() expects 1 to 3 arguments.",
            getattr(node, "lineno", None),
            getattr(node, "col_offset", None),
        )

    if not all(isinstance(arg, int) for arg in args):
        raise RuntimeFault(
            RuntimeErrorType.TYPE_MISMATCH,
            "range() arguments must be integers.",
            getattr(node, "lineno", None),
            getattr(node, "col_offset", None),
        )

    try:
        return range(*args)
    except ValueError as exc:
        raise RuntimeFault(
            RuntimeErrorType.TYPE_MISMATCH,
            str(exc),
            getattr(node, "lineno", None),
            getattr(node, "col_offset", None),
        ) from exc

