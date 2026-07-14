from dataclasses import dataclass
from enum import Enum
from typing import Any


class RuntimeErrorType(str, Enum):
    DIVISION_BY_ZERO = "DivisionByZero"
    INFINITE_LOOP = "InfiniteLoop"
    INDEX_ERROR = "IndexError"
    KEY_ERROR = "KeyError"
    RECURSION_LIMIT = "RecursionLimit"
    TYPE_MISMATCH = "TypeMismatch"
    UNDEFINED_VARIABLE = "UndefinedVariable"
    UNSUPPORTED_OPERATION = "UnsupportedOperation"
    UNSUPPORTED_SYNTAX = "UnsupportedSyntax"


@dataclass(frozen=True)
class RuntimeFault(Exception):
    error_type: RuntimeErrorType
    message: str
    line: int | None = None
    column: int | None = None


@dataclass(frozen=True)
class ReturnSignal(Exception):
    value: Any
