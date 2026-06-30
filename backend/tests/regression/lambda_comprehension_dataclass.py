from dataclasses import dataclass


@dataclass
class Point:
    x: int


transform = lambda item: item + 1  # noqa: E731
values = [value for value in range(3) if value > 0]
