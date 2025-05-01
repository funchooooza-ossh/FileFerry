import asyncio
from collections.abc import Coroutine
from typing import Any

from loguru import logger

from contracts.infrastructure import TaskSchedulerContract


class AsyncioTaskScheduler(TaskSchedulerContract):
    def __init__(self) -> None:
        self._tasks: set[asyncio.Task[Any]] = set()
        self._lock = asyncio.Lock()

    def schedule(self, coro: Coroutine[Any, Any, Any]) -> None:
        task = asyncio.create_task(coro)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

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
                still_running_tasks = [t for t in tasks if not t.done()]
                logger.warning(
                    f"[SCHEDULER][SHUTDOWN] {len(still_running_tasks)} tasks still not finished"
                )
