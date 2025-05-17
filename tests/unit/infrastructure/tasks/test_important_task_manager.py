import asyncio

import pytest
from infrastructure.tasks.manager import ImportantTaskManager


@pytest.mark.asyncio
@pytest.mark.unit
async def test_schedule_and_snapshot() -> None:
    manager = ImportantTaskManager()

    async def task() -> None:
        await asyncio.sleep(0.1)

    await manager.schedule("t1", task)
    snapshot = manager.snapshot()

    assert "t1" in snapshot.get("task_keys")
    assert snapshot.get("active_task_count") == 1
    assert snapshot.get("total_task_count") == 1


@pytest.mark.asyncio
@pytest.mark.unit
async def test_deduplication() -> None:
    manager = ImportantTaskManager()

    async def task() -> None:
        await asyncio.sleep(0.2)

    await manager.schedule("dup", task)
    await manager.schedule("dup", task)

    snapshot = manager.snapshot()
    assert snapshot.get("active_task_count") == 1
    assert snapshot.get("total_task_count") == 1


@pytest.mark.asyncio
@pytest.mark.unit
async def test_max_tasks_limit() -> None:
    manager = ImportantTaskManager(max_tasks=2)

    async def sleeper() -> None:
        await asyncio.sleep(0.5)

    await manager.schedule("k1", sleeper)
    await manager.schedule("k2", sleeper)
    await manager.schedule("k3", sleeper)

    snapshot = manager.snapshot()
    assert "k3" not in snapshot.get("task_keys")
    assert snapshot.get("active_task_count") == 2
    assert snapshot.get("total_task_count") == 2


@pytest.mark.asyncio
@pytest.mark.unit
async def test_on_done_callback_called() -> None:
    manager = ImportantTaskManager()
    called: list[tuple[str, Exception | None]] = []

    async def trivial() -> None:
        await asyncio.sleep(0.01)

    def on_done(key: str, exc: Exception | None) -> None:
        called.append((key, exc))

    await manager.schedule("cb", trivial, on_done)
    await asyncio.sleep(0.05)

    assert called and called[0][0] == "cb"
    assert called[0][1] is None


@pytest.mark.asyncio
@pytest.mark.unit
async def test_shutdown_cancels_tasks() -> None:
    manager = ImportantTaskManager()

    async def blocker() -> None:
        await asyncio.Event().wait()

    await manager.schedule("block", blocker)
    await asyncio.sleep(0.05)
    await manager.shutdown()

    assert manager.snapshot().get("active_task_count") == 0
