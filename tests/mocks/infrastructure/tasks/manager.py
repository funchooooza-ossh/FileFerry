import asyncio
from collections.abc import Callable, Coroutine
from typing import Any

import pytest
from contracts.infrastructure import ImportantTaskManagerContract
from infrastructure.types.task_snapshot import ManagerSnapshot


class FakeImportantTaskManager(ImportantTaskManagerContract):
    def __init__(self):
        self._tasks: dict[str, asyncio.Task[Any]] = {}

    async def schedule(
        self,
        key: str,
        task_factory: Callable[[], Coroutine[Any, Any, Any]],
        on_done: Callable[[str, Exception | None], None] | None = None,
    ) -> None:
        self._tasks[key] = asyncio.create_task(task_factory())

    async def snapshot(self) -> ManagerSnapshot:  # type: ignore
        ...


@pytest.fixture(scope="session")
def mock_task_manager() -> FakeImportantTaskManager:
    return FakeImportantTaskManager()
