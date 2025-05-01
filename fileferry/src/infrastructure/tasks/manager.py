import asyncio
from collections.abc import Callable, Coroutine
from typing import Any

from loguru import logger

from contracts.infrastructure import ImportantTaskManagerContract


class ImportantTaskManager(ImportantTaskManagerContract):
    def __init__(self, max_tasks: int = 100) -> None:
        self._tasks: dict[str, asyncio.Task[Any]] = {}
        self._meta: dict[str, float] = {}
        self._lock = asyncio.Lock()
        self._max_tasks = max_tasks

    async def schedule(
        self,
        key: str,
        task_factory: Callable[[], Coroutine[Any, Any, Any]],
        event: asyncio.Event,
        on_done: Callable[[str, Exception | None], None] | None = None,
    ) -> None:
        async with self._lock:
            if key in self._tasks:
                logger.info(f"[TASK_MANAGER] Task already exists {key}")
                return

            if len(self._tasks) >= self._max_tasks:
                logger.warning(
                    f"[TASK_MANAGER] Limit exceeded ({self._max_tasks}), skipping key={key}"
                )
                return

            async def _runner() -> None:
                exc: Exception | None = None
                try:
                    await task_factory()
                except Exception as e:
                    logger.exception(f"[TASK_MANAGER] Task {key} failed: {e}")
                    exc = e
                finally:
                    self._tasks.pop(key, None)
                    self._meta.pop(key, None)
                    if on_done:
                        try:
                            on_done(key, exc)
                        except Exception as callback_err:
                            logger.exception(
                                f"[TASK_MANAGER] on_done failed for {key}: {callback_err}"
                            )

            task = asyncio.create_task(_runner())
            self._tasks[key] = task
            self._meta[key] = asyncio.get_event_loop().time()

    def has(self, key: str) -> bool:
        return key in self._tasks

    def keys(self) -> list[str]:
        return list(self._tasks.keys())

    def count(self) -> int:
        return len(self._tasks)

    def age(self, key: str) -> float | None:
        ts = self._meta.get(key)
        return (asyncio.get_event_loop().time() - ts) if ts else None
