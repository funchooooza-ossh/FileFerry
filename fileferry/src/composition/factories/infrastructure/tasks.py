from contracts.infrastructure import (
    FileMetaCacheStorageContract,
    ImportantTaskManagerContract,
)
from infrastructure.tasks.consistence import CacheInvalidator
from infrastructure.tasks.manager import ImportantTaskManager, NoOpImportantTaskManager
from infrastructure.tasks.scheduler import AsyncioFireAndForget


def task_manager_factory(
    with_cache: bool,
) -> ImportantTaskManager | NoOpImportantTaskManager:
    if not with_cache:
        return NoOpImportantTaskManager()
    return ImportantTaskManager()


def task_fire_n_forget_factory(with_cache: bool) -> AsyncioFireAndForget | None:
    if not with_cache:
        return None
    return AsyncioFireAndForget()


def cache_invalidator_factory(
    storage: FileMetaCacheStorageContract | None,
    manager: ImportantTaskManagerContract | None,
    retry_interval: float = 5.0,
) -> CacheInvalidator | None:
    if not storage or not manager:
        return None
    return CacheInvalidator(
        cache_storage=storage, task_manager=manager, retry_interval=retry_interval
    )
