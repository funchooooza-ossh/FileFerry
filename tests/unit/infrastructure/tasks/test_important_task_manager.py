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


@pytest.mark.asyncio
@pytest.mark.unit
async def test_skip_if_key_already_scheduled():
    manager = ImportantTaskManager()

    triggered = 0

    async def task_factory():
        nonlocal triggered
        triggered += 1
        await asyncio.sleep(0.01)

    await manager.schedule("same", task_factory)
    await manager.schedule("same", task_factory)
    await asyncio.sleep(0.05)

    assert triggered == 1
    assert manager.snapshot().get("total_task_count") == 1


@pytest.mark.asyncio
@pytest.mark.unit
async def test_task_removal_from_internal_maps():
    manager = ImportantTaskManager()

    async def quick_task():
        await asyncio.sleep(0.01)

    await manager.schedule("removable", quick_task)
    await asyncio.sleep(0.05)

    snapshot = manager.snapshot()
    assert "removable" not in snapshot.get("task_keys")
    assert manager._count() == 0  # type: ignore


@pytest.mark.asyncio
@pytest.mark.unit
async def test_age_returns_zero_if_key_missing():
    manager = ImportantTaskManager()
    age = manager._age("nonexistent")  # type: ignore
    assert age == 0


@pytest.mark.asyncio
@pytest.mark.unit
async def test_on_done_called_with_exception():
    manager = ImportantTaskManager()
    result: list[tuple[str, Exception | None]] = []

    async def failing_task():
        raise RuntimeError("boom")

    def on_done(key: str, exc: Exception | None):
        result.append((key, exc))

    await manager.schedule("fail", failing_task, on_done)
    await asyncio.sleep(0.05)

    assert result
    assert result[0][0] == "fail"
    assert isinstance(result[0][1], RuntimeError)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_total_task_count_increments():
    manager = ImportantTaskManager()

    async def t1():
        pass

    async def t2():
        pass

    async def t3():
        pass

    await manager.schedule("a", t1)
    await manager.schedule("b", t2)
    await manager.schedule("c", t3)

    await asyncio.sleep(0.05)
    snapshot = manager.snapshot()

    assert snapshot.get("total_task_count") == 3
