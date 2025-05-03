import asyncio
import contextlib
from collections.abc import Coroutine
from typing import Any


def wrap_with_event_timeout(
    task: Coroutine[Any, Any, Any], event: asyncio.Event, timeout: float
) -> Coroutine[Any, Any, None]:
    async def wrapped() -> None:
        timeout_task = asyncio.create_task(_trigger_event_after_timeout(event, timeout))
        try:
            await task
        finally:
            timeout_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await timeout_task

    return wrapped()


async def _trigger_event_after_timeout(
    event: asyncio.Event,
    timeout: float,  # noqa: ASYNC109
) -> None:
    await asyncio.sleep(timeout)
    if not event.is_set():
        event.set()
