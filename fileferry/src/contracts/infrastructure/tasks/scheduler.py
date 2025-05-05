from collections.abc import Coroutine
from typing import Any, Protocol, TypeVar

T = TypeVar("T")


class FireAndForgetTasksContract(Protocol):
    """
    Контракт для вынесения любого рода задач в background.
    """

    def schedule(self, coro: Coroutine[Any, Any, T]) -> None: ...
    async def shutdown(self, timeout: float) -> None: ...  # noqa: ASYNC109
