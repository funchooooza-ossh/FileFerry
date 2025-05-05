import asyncio
import contextlib
from collections.abc import Callable, Coroutine
from typing import Any, Optional

from contracts.infrastructure import ImportantTaskManagerContract


class ImportantTaskManager(ImportantTaskManagerContract):
    """
    Имплементация контракта ImportantTaskManagerContract.
    Являет собой продолжение спорного решения, касательно инвалидации
    кэша любой ценой.
    """

    def __init__(self, max_tasks: int = 100) -> None:
        self._tasks: dict[str, asyncio.Task[Any]] = {}
        self._meta: dict[str, float] = {}
        self._lock = asyncio.Lock()
        self._max_tasks = max_tasks

    async def schedule(
        self,
        key: str,
        task_factory: Callable[[], Coroutine[Any, Any, Any]],
        on_done: Optional[Callable[[str, Exception | None], None]] = None,
    ) -> None:
        async with self._lock:
            if key in self._tasks:
                return

            if len(self._tasks) >= self._max_tasks:
                return

            async def _runner() -> None:
                exc: Exception | None = None
                try:
                    await task_factory()
                except Exception as e:
                    exc = e
                finally:
                    self._tasks.pop(key, None)
                    self._meta.pop(key, None)
                    if on_done:
                        with contextlib.suppress(Exception):
                            on_done(key, exc)

            task = asyncio.create_task(_runner())
            self._tasks[key] = task
            self._meta[key] = asyncio.get_running_loop().time()

    def has(self, key: str) -> bool:
        return key in self._tasks

    def keys(self) -> list[str]:
        return list(self._tasks.keys())

    def count(self) -> int:
        return len(self._tasks)

    def age(self, key: str) -> Optional[float]:
        ts = self._meta.get(key)
        return (asyncio.get_running_loop().time() - ts) if ts else None

    async def shutdown(self) -> None:
        for task in self._tasks.values():
            task.cancel()
        await asyncio.gather(*self._tasks.values(), return_exceptions=True)
