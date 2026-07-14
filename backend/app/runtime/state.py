from dataclasses import dataclass, field
from typing import Any


@dataclass
class RuntimeFrame:
    name: str
    variables: dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimeState:
    frames: list[RuntimeFrame] = field(default_factory=lambda: [RuntimeFrame("global")])
    output: list[str] = field(default_factory=list)
    call_stack: list[str] = field(default_factory=list)

    @property
    def current_frame(self) -> RuntimeFrame:
        return self.frames[-1]

    def push_frame(self, name: str) -> None:
        self.frames.append(RuntimeFrame(name))
        self.call_stack.append(name)

    def pop_frame(self) -> None:
        if len(self.frames) > 1:
            self.frames.pop()
        if self.call_stack:
            self.call_stack.pop()

    def define(self, name: str, value: Any) -> None:
        self.current_frame.variables[name] = value

    def assign(self, name: str, value: Any) -> None:
        for frame in reversed(self.frames):
            if name in frame.variables:
                frame.variables[name] = value
                return
        self.current_frame.variables[name] = value

    def resolve(self, name: str) -> Any:
        for frame in reversed(self.frames):
            if name in frame.variables:
                return frame.variables[name]
        raise KeyError(name)

    def snapshot(self) -> dict[str, str]:
        values: dict[str, Any] = {}
        for frame in self.frames:
            values.update(frame.variables)
        return {
            name: self.format_value(value)
            for name, value in values.items()
            if not callable(value)
        }

    def format_value(self, value: Any) -> str:
        if isinstance(value, str):
            return value
        return repr(value)

