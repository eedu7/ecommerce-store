from abc import ABC, abstractmethod
from typing import Callable


class BaseKeyMaker(ABC):
    @abstractmethod
    async def make(self, func: Callable, prefix: str) -> str:
        pass
