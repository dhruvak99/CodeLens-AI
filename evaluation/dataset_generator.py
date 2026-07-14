from __future__ import annotations

import ast
import random
from dataclasses import dataclass


SEED = 20260703


@dataclass(frozen=True)
class CategorySpec:
    name: str
    expected: list[str]
    count: int


CATEGORY_SPECS = [
    CategorySpec("Correct Programs", [], 200),
    CategorySpec("Undefined Variable", ["UndefinedVariable"], 100),
    CategorySpec("Infinite Loop", ["InfiniteLoop"], 100),
    CategorySpec("Missing Recursion Base Case", ["MissingBaseCase"], 100),
    CategorySpec("Binary Search Logic Error", ["BinarySearchLogicError"], 100),
    CategorySpec("Unreachable Code", ["UnreachableCode"], 100),
    CategorySpec("Unused Variable", ["UnusedVariable"], 100),
    CategorySpec("Missing Return", ["MissingReturn"], 100),
    CategorySpec("Shadowed Variable", ["ShadowedVariable"], 50),
    CategorySpec("Dangerous Import", ["DangerousImport"], 50),
]


NAMES = [
    "score",
    "total",
    "index",
    "value",
    "count",
    "target",
    "number",
    "item",
    "result",
    "current",
    "limit",
    "answer",
]
FUNC_NAMES = [
    "solve",
    "process_values",
    "search_item",
    "count_items",
    "build_result",
    "calculate_total",
    "student_solution",
    "run_example",
]


def generate_dataset() -> list[dict[str, object]]:
    rng = random.Random(SEED)
    records: list[dict[str, object]] = []
    used_codes: set[str] = set()
    record_id = 1

    for spec in CATEGORY_SPECS:
        generator = _generator_for(spec.name)
        for local_index in range(spec.count):
            code = _unique_valid_code(
                lambda attempt: generator(local_index, attempt, rng),
                used_codes,
            )
            records.append(
                {
                    "id": record_id,
                    "category": spec.name,
                    "expected": list(spec.expected),
                    "code": code,
                }
            )
            record_id += 1

    return records


def _unique_valid_code(make_code: object, used_codes: set[str]) -> str:
    for attempt in range(200):
        code = make_code(attempt)  # type: ignore[operator]
        ast.parse(code)
        if code not in used_codes:
            used_codes.add(code)
            return code
    raise RuntimeError("Unable to generate a unique valid program.")


def _generator_for(name: str) -> object:
    return {
        "Correct Programs": _correct_program,
        "Undefined Variable": _undefined_variable_program,
        "Infinite Loop": _infinite_loop_program,
        "Missing Recursion Base Case": _missing_base_case_program,
        "Binary Search Logic Error": _binary_search_error_program,
        "Unreachable Code": _unreachable_code_program,
        "Unused Variable": _unused_variable_program,
        "Missing Return": _missing_return_program,
        "Shadowed Variable": _shadowed_variable_program,
        "Dangerous Import": _dangerous_import_program,
    }[name]


def _name(rng: random.Random, index: int, prefix: str = "") -> str:
    base = rng.choice(NAMES)
    return f"{prefix}{base}_{index}"


def _function(rng: random.Random, index: int) -> str:
    return f"{rng.choice(FUNC_NAMES)}_{index}"


def _header(category: str, index: int, attempt: int) -> str:
    return f"# CodeLens benchmark: {category} case {index}-{attempt}\n"


def _correct_program(index: int, attempt: int, rng: random.Random) -> str:
    family = (index + attempt) % 10
    fn = _function(rng, index)
    arr = _name(rng, index, "data_")
    target = _name(rng, index, "target_")
    if family == 0:
        return (
            _header("correct binary search", index, attempt)
            + f"def {fn}({arr}, {target}):\n"
            f"    low = 0\n"
            f"    high = len({arr}) - 1\n"
            f"    while low <= high:\n"
            f"        mid = (low + high) // 2\n"
            f"        if {arr}[mid] == {target}:\n"
            f"            return mid\n"
            f"        if {arr}[mid] < {target}:\n"
            f"            low = mid + 1\n"
            f"        else:\n"
            f"            high = mid - 1\n"
            f"    return -1\n\n"
            f"position = {fn}([1, 3, 5, 7, 9], 7)\n"
            f"print(position)\n"
        )
    if family == 1:
        return (
            _header("correct linear search", index, attempt)
            + f"def {fn}({arr}, {target}):\n"
            f"    for position in range(len({arr})):\n"
            f"        if {arr}[position] == {target}:\n"
            f"            return position\n"
            f"    return -1\n\n"
            f"answer = {fn}([4, 8, 12, 16], 12)\n"
            f"print(answer)\n"
        )
    if family == 2:
        return (
            _header("correct factorial", index, attempt)
            + f"def {fn}(number):\n"
            f"    if number <= 1:\n"
            f"        return 1\n"
            f"    return number * {fn}(number - 1)\n\n"
            f"print({fn}(5))\n"
        )
    if family == 3:
        return (
            _header("correct counting", index, attempt)
            + f"def {fn}({arr}):\n"
            f"    total = 0\n"
            f"    for value in {arr}:\n"
            f"        if value % 2 == 0:\n"
            f"            total += 1\n"
            f"    return total\n\n"
            f"print({fn}([2, 5, 6, 7, 8]))\n"
        )
    if family == 4:
        return (
            _header("correct stack", index, attempt)
            + f"stack = []\n"
            f"for value in [1, 2, 3]:\n"
            f"    stack.append(value)\n"
            f"top_value = stack.pop()\n"
            f"print(top_value)\n"
        )
    if family == 5:
        return (
            _header("correct dictionary", index, attempt)
            + f"student = {{'name': 'Asha', 'score': 88}}\n"
            f"bonus = 5\n"
            f"student['score'] = student['score'] + bonus\n"
            f"print(student['score'])\n"
        )
    if family == 6:
        return (
            _header("correct matrix traversal", index, attempt)
            + f"matrix = [[1, 2], [3, 4], [5, 6]]\n"
            f"total = 0\n"
            f"for row in matrix:\n"
            f"    for value in row:\n"
            f"        total += value\n"
            f"print(total)\n"
        )
    if family == 7:
        return (
            _header("correct tuple use", index, attempt)
            + f"point = (3, 5)\n"
            f"x_value = point[0]\n"
            f"y_value = point[1]\n"
            f"print(x_value + y_value)\n"
        )
    if family == 8:
        return (
            _header("correct insertion style pass", index, attempt)
            + f"numbers = [5, 2, 4, 1]\n"
            f"ordered = []\n"
            f"for value in numbers:\n"
            f"    ordered.append(value)\n"
            f"ordered.sort()\n"
            f"print(ordered[0])\n"
        )
    return (
        _header("correct fibonacci", index, attempt)
        + f"def {fn}(number):\n"
        f"    if number <= 1:\n"
        f"        return number\n"
        f"    first = 0\n"
        f"    second = 1\n"
        f"    for step in range(2, number + 1):\n"
        f"        first, second = second, first + second\n"
        f"    return second\n\n"
        f"print({fn}(7))\n"
    )


def _undefined_variable_program(index: int, attempt: int, rng: random.Random) -> str:
    missing = _name(rng, index, "missing_")
    fn = _function(rng, index)
    variants = [
        f"print({missing})\n",
        f"def {fn}():\n    return {missing}\n\nprint({fn}())\n",
        f"total = 10\nanswer = total + {missing}\nprint(answer)\n",
        f"def {fn}(items):\n    count = len(items)\n    return count + {missing}\n\nprint({fn}([1, 2]))\n",
    ]
    return _header("undefined variable", index, attempt) + variants[(index + attempt) % len(variants)]


def _infinite_loop_program(index: int, attempt: int, rng: random.Random) -> str:
    var = _name(rng, index, "counter_")
    variants = [
        f"{var} = 0\nwhile True:\n    print({var})\n    {var} += 1\n",
        f"{var} = 5\nwhile {var} > 0:\n    print({var})\n",
        f"{var} = 1\nwhile {var} == {var}:\n    {var} += 1\n",
        f"{var} = 10\nwhile {var} < 20:\n    {var} -= 1\n",
    ]
    return _header("infinite loop", index, attempt) + variants[(index + attempt) % len(variants)]


def _missing_base_case_program(index: int, attempt: int, rng: random.Random) -> str:
    fn = f"recursive_task_{index}"
    variants = [
        f"def {fn}(number):\n    return {fn}(number - 1)\n\nprint({fn}(3))\n",
        f"def {fn}(items):\n    print(len(items))\n    return {fn}(items[1:])\n\n{fn}([1, 2, 3])\n",
        f"def {fn}(value):\n    next_value = value + 1\n    return {fn}(next_value)\n\n{fn}(0)\n",
    ]
    return _header("missing recursion base case", index, attempt) + variants[(index + attempt) % len(variants)]


def _binary_search_error_program(index: int, attempt: int, rng: random.Random) -> str:
    fn = f"binary_search_student_{index}"
    wrong_update = [
        "            high = mid + 1\n",
        "            high = mid - 1\n",
        "            low = mid - 1\n",
        "            return low\n",
    ][(index + attempt) % 4]
    return (
        _header("binary search logic error", index, attempt)
        + f"def {fn}(values, target):\n"
        f"    low = 0\n"
        f"    high = len(values) - 1\n"
        f"    while low <= high:\n"
        f"        mid = (low + high) // 2\n"
        f"        if values[mid] == target:\n"
        f"            return mid\n"
        f"        if values[mid] < target:\n"
        f"{wrong_update}"
        f"        else:\n"
        f"            high = mid - 1\n"
        f"    return -1\n\n"
        f"print({fn}([1, 3, 5, 7], 5))\n"
    )


def _unreachable_code_program(index: int, attempt: int, rng: random.Random) -> str:
    fn = _function(rng, index)
    variants = [
        f"def {fn}(value):\n    return value * 2\n    print('never runs')\n\nprint({fn}(4))\n",
        f"def {fn}(items):\n    for item in items:\n        break\n        print(item)\n    return len(items)\n\nprint({fn}([1, 2]))\n",
        f"def {fn}(items):\n    for item in items:\n        continue\n        print(item)\n    return 0\n\nprint({fn}([1, 2]))\n",
        f"def {fn}():\n    raise ValueError('stop')\n    print('after raise')\n\n# {fn} is intentionally not called in this benchmark\n",
    ]
    return _header("unreachable code", index, attempt) + variants[(index + attempt) % len(variants)]


def _unused_variable_program(index: int, attempt: int, rng: random.Random) -> str:
    unused = _name(rng, index, "draft_")
    fn = _function(rng, index)
    variants = [
        f"def {fn}(values):\n    {unused} = len(values) + 10\n    total = 0\n    for value in values:\n        total += value\n    return total\n\nprint({fn}([1, 2, 3]))\n",
        f"{unused} = 'temporary note'\nanswer = 42\nprint(answer)\n",
        f"def {fn}():\n    {unused} = [1, 2, 3]\n    message = 'done'\n    return message\n\nprint({fn}())\n",
    ]
    return _header("unused variable", index, attempt) + variants[(index + attempt) % len(variants)]


def _missing_return_program(index: int, attempt: int, rng: random.Random) -> str:
    fn = _function(rng, index)
    variants = [
        f"def {fn}(score):\n    if score >= 50:\n        return 'pass'\n\nprint({fn}(30))\n",
        f"def {fn}(items):\n    if len(items) == 0:\n        return 0\n    total = 0\n    for item in items:\n        total += item\n\nprint({fn}([1, 2]))\n",
        f"def {fn}(flag):\n    if flag:\n        return 1\n    else:\n        value = 0\n        print(value)\n\nprint({fn}(False))\n",
    ]
    return _header("missing return", index, attempt) + variants[(index + attempt) % len(variants)]


def _shadowed_variable_program(index: int, attempt: int, rng: random.Random) -> str:
    outer = _name(rng, index, "shared_")
    fn = _function(rng, index)
    variants = [
        f"{outer} = 10\n\ndef {fn}():\n    {outer} = 5\n    return {outer}\n\nprint({fn}())\n",
        f"def {fn}():\n    {outer} = 'outer'\n    def helper():\n        {outer} = 'inner'\n        return {outer}\n    return helper()\n\nprint({fn}())\n",
    ]
    return _header("shadowed variable", index, attempt) + variants[(index + attempt) % len(variants)]


def _dangerous_import_program(index: int, attempt: int, rng: random.Random) -> str:
    module = ["os", "subprocess", "shutil", "pickle"][(index + attempt) % 4]
    alias = f"{module}_tool_{index}"
    variants = [
        f"import {module}\n\nprint('loaded {module}')\n",
        f"import {module} as {alias}\n\nprint('student helper ready')\n",
        f"from {module} import *\n\nprint('wildcard import used')\n",
    ]
    return _header("dangerous import", index, attempt) + variants[(index + attempt) % len(variants)]

