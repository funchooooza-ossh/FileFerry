import pytest
from infrastructure.tasks.manager import ImportantTaskManager
from infrastructure.tasks.scheduler import AsyncioFireAndForget


@pytest.fixture(scope="function")
def task_scheduler() -> AsyncioFireAndForget:
    return AsyncioFireAndForget()


@pytest.fixture(scope="function")
def task_manager() -> ImportantTaskManager:
    return ImportantTaskManager()
