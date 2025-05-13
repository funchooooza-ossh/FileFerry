import asyncio

import pytest
from infrastructure.tasks.scheduler import AsyncioFireAndForget


@pytest.mark.unit
@pytest.mark.asyncio
async def test_fire_n_forget_schedule():
    scheduler = AsyncioFireAndForget(max_tasks=5)

    ran = asyncio.Event()

    async def coro():
        ran.set()

    scheduler.schedule(coro())
    await asyncio.wait_for(ran.wait(), timeout=1.0)

    await asyncio.sleep(0)
    assert len(scheduler._tasks) == 0  # type: ignore


@pytest.mark.asyncio
async def test_schedule_limit(caplog: pytest.LogCaptureFixture) -> None:
    scheduler = AsyncioFireAndForget(max_tasks=1)

    async def dummy():
        await asyncio.sleep(0.1)

    scheduler.schedule(dummy())

    scheduler.schedule(dummy())

    await asyncio.sleep(0.2)

    assert "[SCHEDULER] Task limit exceeded" in caplog.text


@pytest.mark.asyncio
async def test_shutdown_cancels_tasks(caplog: pytest.LogCaptureFixture) -> None:
    scheduler = AsyncioFireAndForget()

    async def long_running():
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            await asyncio.sleep(1000)

    scheduler.schedule(long_running())

    await asyncio.sleep(0.1)
    await scheduler.shutdown(timeout=1.0)

    assert len(scheduler._tasks) == 0  # type: ignore


@pytest.mark.asyncio
async def test_shutdown_timeout_logged(caplog: pytest.LogCaptureFixture) -> None:
    scheduler = AsyncioFireAndForget()

    async def never_finishes():
        await asyncio.Event().wait()

    scheduler.schedule(never_finishes())

    await asyncio.sleep(0.1)
    caplog.set_level("WARNING")
    await scheduler.shutdown(timeout=0.0)

    assert any(
        "[SCHEDULER] Shutdown timeout" in rec.message
        for rec in caplog.records
        if rec.levelname == "WARNING"
    )
