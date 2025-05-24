import asyncio
from unittest.mock import AsyncMock

import pytest
from infrastructure.tasks.consistence import CacheInvalidator
from redis.exceptions import RedisError


@pytest.mark.asyncio
@pytest.mark.unit
async def test_invalidate_success_immediately(mock_task_manager: AsyncMock):
    storage = AsyncMock()
    manager = mock_task_manager

    invalidator = CacheInvalidator(storage, manager, retry_interval=0.01)

    done = await invalidator.invalidate("file123", max_retry_seconds=0.1)
    await asyncio.wait_for(done.wait(), timeout=0.2)

    storage.delete.assert_awaited_once_with("file123")


@pytest.mark.asyncio
@pytest.mark.unit
async def test_invalidate_with_retries(mock_task_manager: AsyncMock):
    storage = AsyncMock()
    storage.delete.side_effect = [RedisError(), RedisError(), AsyncMock()]
    manager = mock_task_manager

    invalidator = CacheInvalidator(storage, manager, retry_interval=0.01)

    done = await invalidator.invalidate("file-retry", max_retry_seconds=0.1)
    await asyncio.wait_for(done.wait(), timeout=0.3)

    assert storage.delete.await_count >= 3


@pytest.mark.asyncio
@pytest.mark.unit
async def test_invalidate_timeout(mock_task_manager: AsyncMock):
    storage = AsyncMock()
    storage.delete.side_effect = RedisError("always fails")
    manager = mock_task_manager

    invalidator = CacheInvalidator(storage, manager, retry_interval=0.01)

    done = await invalidator.invalidate("timeout-file", max_retry_seconds=0.05)
    await asyncio.wait_for(done.wait(), timeout=0.3)

    assert done.is_set()
    assert storage.delete.await_count >= 1
