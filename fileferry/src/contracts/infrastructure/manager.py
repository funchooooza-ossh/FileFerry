from collections.abc import Callable, Coroutine
from typing import Any, Protocol

from shared.types.task_manager import ManagerSnapshot


class ImportantTaskManagerContract(Protocol):
    """
    Background manager важных задач, нужен для поддержания существования
    и отслеживания состояния важных bg задач
    """

    async def schedule(
        self,
        key: str,
        task_factory: Callable[[], Coroutine[Any, Any, Any]],
        on_done: Callable[[str, Exception | None], None] | None = None,
    ) -> None: ...

    def snapshot(self) -> ManagerSnapshot:
        """Текущее состояние менеджера задач"""
        ...
