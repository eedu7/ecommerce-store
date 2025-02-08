import inspect
from typing import Callable

from core.cache.base import BaseKeyMaker


class CustomKeyMaker(BaseKeyMaker):
    async def make(self, func: Callable, prefix: str) -> str:
        path = f"{prefix}::{inspect.getmodule(func).__name__}.{function.__name__}"
        args = ""

        for arg in inspect.signature(func).parameters.values():
            args += arg.name

        if args:
            return f"{path}.{args}"

        return path
