from abc import ABC, abstractmethod

from app.fixes.models import FixAction, FixContext
from app.fixes.registry import FixRegistry


class BaseFix(ABC):
    finding_type: str

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if not getattr(cls, "abstract", False):
            FixRegistry.register(cls)

    @abstractmethod
    def action(self, context: FixContext) -> FixAction | None:
        raise NotImplementedError
