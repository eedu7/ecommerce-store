from abc import ABC, abstractmethod
from collections.abc import Callable


class BaseKeyMaker(ABC):
    @abstractmethod
    async def make(self, func: Callable, prefix: str) -> str:
        pass
