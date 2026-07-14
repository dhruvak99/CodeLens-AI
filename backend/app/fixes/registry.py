from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.fixes.base import BaseFix


class FixRegistry:
    _fixes: list[type["BaseFix"]] = []

    @classmethod
    def register(cls, fix: type["BaseFix"]) -> None:
        if fix not in cls._fixes:
            cls._fixes.append(fix)

    @classmethod
    def fixes(cls) -> list[type["BaseFix"]]:
        return list(cls._fixes)
