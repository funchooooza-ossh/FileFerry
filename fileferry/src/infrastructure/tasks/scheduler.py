import asyncio
from collections.abc import Coroutine
from typing import Any

from loguru import logger

from contracts.infrastructure import FireAndForgetTasksContract


class AsyncioFireAndForget(FireAndForgetTasksContract):
    """
    Имплементация FireAndForget через asyncio.Task
    """

    def __init__(self, max_tasks: int = 1000) -> None:
        self._tasks: set[asyncio.Task[Any]] = set()
        self._lock = asyncio.Lock()
        self._max_tasks = max_tasks

    def schedule(self, coro: Coroutine[Any, Any, Any]) -> None:
        if len(self._tasks) >= self._max_tasks:
            logger.warning(
                f"[SCHEDULER] Task limit exceeded ({self._max_tasks}), skipping task"
            )
            return

        loop = asyncio.get_running_loop()
        task = loop.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._on_done)

    def _on_done(self, task: asyncio.Task[Any]) -> None:
        self._tasks.discard(task)

    async def shutdown(self, timeout: float = 5.0) -> None:  # noqa: ASYNC109
        async with self._lock:
            tasks = list(self._tasks)
            for task in tasks:
                task.cancel()

            try:
                await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True), timeout
                )
            except TimeoutError:
                still_running = [t for t in tasks if not t.done()]
                logger.warning(
                    f"[SCHEDULER] Shutdown timeout, {len(still_running)} tasks still running"
                )
