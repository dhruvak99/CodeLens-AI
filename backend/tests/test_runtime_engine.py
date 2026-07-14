from typing import Any, cast

from app.schemas.runtime import RuntimeRequest
from app.services.runtime_service import RuntimeService


def execute(code: str) -> dict[str, object]:
    return RuntimeService().get_runtime_trace(RuntimeRequest(code=code)).model_dump(
        by_alias=True
    )


def test_runtime_prints_variable() -> None:
    response = execute("x = 5\nprint(x)\n")

    assert response["success"] is True
    assert response["output"] == ["5"]
    assert response["steps"][-1]["output"] == ["5"]  # type: ignore[index]


def test_runtime_arithmetic_assignment() -> None:
    response = execute("x = 5\ny = x + 10\nprint(y)\n")

    assert response["success"] is True
    assert response["output"] == ["15"]
    assert response["steps"][1]["changedVariable"] == "y"  # type: ignore[index]
    assert response["steps"][1]["variables"]["y"] == "15"  # type: ignore[index]


def test_runtime_for_range_loop() -> None:
    response = execute("for i in range(3):\n    print(i)\n")

    assert response["success"] is True
    assert response["output"] == ["0", "1", "2"]


def test_runtime_while_loop() -> None:
    response = execute("x = 3\nwhile x > 0:\n    print(x)\n    x -= 1\n")

    assert response["success"] is True
    assert response["output"] == ["3", "2", "1"]
    assert response["steps"][-1]["variables"]["x"] == "0"  # type: ignore[index]


def test_runtime_recursive_factorial() -> None:
    response = execute(
        "def factorial(n):\n"
        "    if n <= 1:\n"
        "        return 1\n"
        "    return n * factorial(n - 1)\n"
        "\n"
        "result = factorial(5)\n"
        "print(result)\n"
    )

    assert response["success"] is True
    assert response["output"] == ["120"]


def test_runtime_division_by_zero() -> None:
    response = execute("x = 1 / 0\n")

    assert response["success"] is False
    assert response["steps"] == []
    assert response["error"]["type"] == "DivisionByZero"  # type: ignore[index]


def test_runtime_rejects_import() -> None:
    response = execute("import os\n")

    assert response["success"] is False
    assert response["error"]["type"] == "UnsupportedSyntax"  # type: ignore[index]


def test_runtime_rejects_open_call() -> None:
    response = execute("open('secret.txt')\n")

    assert response["success"] is False
    assert response["error"]["type"] == "UnsupportedSyntax"  # type: ignore[index]


def test_runtime_rejects_class() -> None:
    response = execute("class Box:\n    pass\n")

    assert response["success"] is False
    assert response["error"]["type"] == "UnsupportedSyntax"  # type: ignore[index]


def test_runtime_infinite_loop_limit() -> None:
    response = execute("x = 1\nwhile x > 0:\n    x += 1\n")

    assert response["success"] is False
    assert response["steps"] == []
    assert response["error"]["type"] == "InfiniteLoop"  # type: ignore[index]
    assert response["error"]["message"] == "Infinite loop limit exceeded."  # type: ignore[index]


def test_runtime_recursion_limit() -> None:
    response = execute("def recurse(n):\n    return recurse(n + 1)\n\nrecurse(0)\n")

    assert response["success"] is False
    assert response["steps"] == []
    assert response["error"]["type"] == "RecursionLimit"  # type: ignore[index]


def test_runtime_list_subscript() -> None:
    response = execute("arr = [10, 20, 30]\nprint(arr[1])\n")

    assert response["success"] is True
    assert response["output"] == ["20"]


def test_runtime_negative_indexing() -> None:
    response = execute("arr = [1, 2, 3]\nprint(arr[-1])\n")

    assert response["success"] is True
    assert response["output"] == ["3"]


def test_runtime_len_list() -> None:
    response = execute("arr = [5, 6, 7]\nprint(len(arr))\n")

    assert response["success"] is True
    assert response["output"] == ["3"]


def test_runtime_tuple_subscript() -> None:
    response = execute("point = (4, 8)\nprint(point[0])\n")

    assert response["success"] is True
    assert response["output"] == ["4"]


def test_runtime_dictionary_subscript() -> None:
    response = execute('student = {"age": 20}\nprint(student["age"])\n')

    assert response["success"] is True
    assert response["output"] == ["20"]


def test_runtime_nested_matrix_subscript() -> None:
    response = execute("matrix = [[1, 2], [3, 4]]\nprint(matrix[1][0])\n")

    assert response["success"] is True
    assert response["output"] == ["3"]


def test_runtime_binary_search_with_subscripts_and_len() -> None:
    response = execute(
        "def binary_search(arr, target):\n"
        "    low = 0\n"
        "    high = len(arr) - 1\n"
        "\n"
        "    while low <= high:\n"
        "        mid = (low + high) // 2\n"
        "\n"
        "        if arr[mid] == target:\n"
        "            return mid\n"
        "\n"
        "        elif arr[mid] < target:\n"
        "            low = mid + 1\n"
        "\n"
        "        else:\n"
        "            high = mid - 1\n"
        "\n"
        "    return -1\n"
        "\n"
        "print(binary_search([1, 3, 5, 7, 9], 7))\n"
    )

    assert response["success"] is True
    assert response["output"] == ["3"]
    steps = cast(list[dict[str, Any]], response["steps"])
    assert any(
        step["changedVariable"] == "mid" and step["variables"]["mid"] == "3"
        for step in steps
    )
    assert any(
        step["changedVariable"] == "return" and step["variables"]["return"] == "3"
        for step in steps
    )


def test_runtime_index_error() -> None:
    response = execute("arr = []\nprint(arr[0])\n")

    assert response["success"] is False
    assert response["steps"] == []
    assert response["error"]["type"] == "IndexError"  # type: ignore[index]


def test_runtime_len_type_mismatch() -> None:
    response = execute("print(len(100))\n")

    assert response["success"] is False
    assert response["steps"] == []
    assert response["error"]["type"] == "TypeMismatch"  # type: ignore[index]


def test_runtime_key_error() -> None:
    response = execute('student = {"age": 20}\nprint(student["name"])\n')

    assert response["success"] is False
    assert response["error"]["type"] == "KeyError"  # type: ignore[index]


def test_runtime_rejects_slice_syntax() -> None:
    response = execute("arr = [1, 2, 3]\nprint(arr[1:2])\n")

    assert response["success"] is False
    assert response["error"]["type"] == "UnsupportedOperation"  # type: ignore[index]
