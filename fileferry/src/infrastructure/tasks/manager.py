import asyncio
import contextlib
from collections.abc import Callable, Coroutine
from typing import Any, Optional

from contracts.infrastructure import ImportantTaskManagerContract
from infrastructure.types.task_snapshot import ManagerSnapshot


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
        self._task_total: int = 0

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

            self._task_total += 1
            task = asyncio.create_task(_runner())
            self._tasks[key] = task
            self._meta[key] = asyncio.get_running_loop().time()

    def snapshot(self) -> ManagerSnapshot:
        task_keys = self._keys()
        task_ages = {k: self._age(k) for k in task_keys}
        active_task_count = self._count()
        total_task_count = self._task_total

        return ManagerSnapshot(
            task_keys=task_keys,
            task_ages=task_ages,
            active_task_count=active_task_count,
            total_task_count=total_task_count,
        )

    def _has(self, key: str) -> bool:
        return key in self._tasks

    def _keys(self) -> list[str]:
        return list(self._tasks.keys())

    def _count(self) -> int:
        return len(self._tasks)

    def _age(self, key: str) -> float:
        try:
            ts = self._meta[key]
            return asyncio.get_running_loop().time() - ts
        except KeyError:
            return 0

    async def shutdown(self) -> None:
        for task in self._tasks.values():
            task.cancel()
        await asyncio.gather(*self._tasks.values(), return_exceptions=True)


class NoOpImportantTaskManager(ImportantTaskManagerContract):
    """
    Класс затычка, на случай, если выключен кэш.
    Не лучшее рещение, но в целом сносное.
    """

    async def schedule(
        self,
        key: str,
        task_factory: Callable[[], Coroutine[Any, Any, Any]],
        on_done: Optional[Callable[[str, Exception | None], None]] = None,
    ) -> None:
        pass

    def has(self, key: str) -> bool:
        return False

    def keys(self) -> list[str]:
        return []

    def count(self) -> int:
        return 0

    def age(self, key: str) -> Optional[float]:
        return None

    async def shutdown(self) -> None:
        pass

    def snapshot(self) -> ManagerSnapshot:
        return ManagerSnapshot(
            active_task_count=0,
            total_task_count=0,
            task_keys=[],
            task_ages={},
        )
