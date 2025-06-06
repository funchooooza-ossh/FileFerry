from unittest.mock import AsyncMock

import pytest
from domain.models import FileMeta
from infrastructure.data_access.redis import CachedFileMetaDataAccess
from infrastructure.tasks.scheduler import AsyncioFireAndForget


@pytest.mark.asyncio
@pytest.mark.unit
async def test_save_schedules_cache_set(
    mock_sql_data_access: AsyncMock,
    mock_redis_storage: AsyncMock,
    mock_cache_invalidator: AsyncMock,
    task_scheduler: AsyncioFireAndForget,
    filemeta: FileMeta,
):
    dao = CachedFileMetaDataAccess(
        invalidator=mock_cache_invalidator,
        storage=mock_redis_storage,
        scheduler=task_scheduler,
        delegate=mock_sql_data_access,
        ttl=100,
    )
    mock_sql_data_access.save.return_value = filemeta

    result = await dao.save(filemeta)

    assert result == filemeta
    mock_redis_storage.set.assert_called_once_with(filemeta, ttl=100)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_invalidates_cache(
    mock_sql_data_access: AsyncMock,
    mock_redis_storage: AsyncMock,
    mock_cache_invalidator: AsyncMock,
    task_scheduler: AsyncioFireAndForget,
    filemeta: FileMeta,
):
    mock_sql_data_access.update.return_value = filemeta

    dao = CachedFileMetaDataAccess(
        invalidator=mock_cache_invalidator,
        storage=mock_redis_storage,
        scheduler=task_scheduler,
        delegate=mock_sql_data_access,
        ttl=200,
    )

    result = await dao.update(filemeta)

    assert result == filemeta
    mock_sql_data_access.update.assert_called_once_with(filemeta)
    mock_cache_invalidator.invalidate.assert_called_once_with(
        filemeta.get_id(), max_retry_seconds=200
    )


@pytest.mark.asyncio
@pytest.mark.unit
async def test_delete_delegates_and_invalidates(
    mock_sql_data_access: AsyncMock,
    mock_redis_storage: AsyncMock,
    mock_cache_invalidator: AsyncMock,
    task_scheduler: AsyncioFireAndForget,
    valid_uuid: str,
):
    dao = CachedFileMetaDataAccess(
        invalidator=mock_cache_invalidator,
        storage=mock_redis_storage,
        scheduler=task_scheduler,
        delegate=mock_sql_data_access,
        ttl=300,
    )

    await dao.delete(valid_uuid)

    mock_sql_data_access.delete.assert_called_once_with(valid_uuid)
    mock_cache_invalidator.invalidate.assert_called_once_with(
        valid_uuid, max_retry_seconds=300
    )


@pytest.mark.asyncio
@pytest.mark.unit
async def test_healthcheck_returns_aggregated_status(
    mock_sql_data_access: AsyncMock,
    mock_redis_storage: AsyncMock,
    mock_cache_invalidator: AsyncMock,
    task_scheduler: AsyncioFireAndForget,
):
    mock_sql_data_access.healthcheck.return_value = {"status": "ok"}
    mock_redis_storage.healthcheck.return_value = {"status": "down"}

    dao = CachedFileMetaDataAccess(
        invalidator=mock_cache_invalidator,
        storage=mock_redis_storage,
        scheduler=task_scheduler,
        delegate=mock_sql_data_access,
        ttl=300,
    )

    status = await dao.healthcheck()

    assert status.get("status") == "degraded"
    assert status.get("details") == {
        "delegate": {"status": "ok"},
        "cache": {"status": "down"},
    }


@pytest.mark.asyncio
@pytest.mark.unit
async def test_save_schedules_cache_write_if_success(
    mock_sql_data_access: AsyncMock,
    mock_redis_storage: AsyncMock,
    mock_cache_invalidator: AsyncMock,
    task_scheduler: AsyncioFireAndForget,
    filemeta: FileMeta,
):
    mock_sql_data_access.save.return_value = filemeta

    dao = CachedFileMetaDataAccess(
        invalidator=mock_cache_invalidator,
        storage=mock_redis_storage,
        scheduler=task_scheduler,
        delegate=mock_sql_data_access,
        ttl=100,
    )

    result = await dao.save(filemeta)

    assert result == filemeta
    mock_redis_storage.set.assert_called_once_with(filemeta, ttl=100)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_save_does_not_schedule_if_none_returned(
    mock_sql_data_access: AsyncMock,
    mock_redis_storage: AsyncMock,
    mock_cache_invalidator: AsyncMock,
    task_scheduler: AsyncioFireAndForget,
    filemeta: FileMeta,
):
    mock_sql_data_access.save.return_value = None

    dao = CachedFileMetaDataAccess(
        invalidator=mock_cache_invalidator,
        storage=mock_redis_storage,
        scheduler=task_scheduler,
        delegate=mock_sql_data_access,
        ttl=100,
    )

    result = await dao.save(filemeta)

    assert result is None
    mock_redis_storage.set.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_returns_cached_value(
    mock_sql_data_access: AsyncMock,
    mock_redis_storage: AsyncMock,
    mock_cache_invalidator: AsyncMock,
    task_scheduler: AsyncioFireAndForget,
    filemeta: FileMeta,
):
    mock_redis_storage.get.return_value = filemeta

    dao = CachedFileMetaDataAccess(
        invalidator=mock_cache_invalidator,
        storage=mock_redis_storage,
        scheduler=task_scheduler,
        delegate=mock_sql_data_access,
        ttl=100,
    )

    result = await dao.get(filemeta.get_id())

    assert result == filemeta
    mock_sql_data_access.get.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_fallbacks_to_delegate_and_sets_cache(
    mock_sql_data_access: AsyncMock,
    mock_redis_storage: AsyncMock,
    mock_cache_invalidator: AsyncMock,
    task_scheduler: AsyncioFireAndForget,
    filemeta: FileMeta,
):
    mock_redis_storage.get.return_value = None
    mock_sql_data_access.get.return_value = filemeta

    dao = CachedFileMetaDataAccess(
        invalidator=mock_cache_invalidator,
        storage=mock_redis_storage,
        scheduler=task_scheduler,
        delegate=mock_sql_data_access,
        ttl=100,
    )

    result = await dao.get(filemeta.get_id())

    assert result == filemeta
    mock_sql_data_access.get.assert_called_once_with(filemeta.get_id())
    mock_redis_storage.set.assert_called_once_with(filemeta, ttl=100)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_get_returns_none_if_delegate_returns_none(
    mock_sql_data_access: AsyncMock,
    mock_redis_storage: AsyncMock,
    mock_cache_invalidator: AsyncMock,
    task_scheduler: AsyncioFireAndForget,
    filemeta: FileMeta,
):
    mock_redis_storage.get.return_value = None
    mock_sql_data_access.get.return_value = None

    dao = CachedFileMetaDataAccess(
        invalidator=mock_cache_invalidator,
        storage=mock_redis_storage,
        scheduler=task_scheduler,
        delegate=mock_sql_data_access,
        ttl=100,
    )

    result = await dao.get("missing-id")

    assert result is None
    mock_redis_storage.set.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_healthcheck_all_ok(
    mock_sql_data_access: AsyncMock,
    mock_redis_storage: AsyncMock,
    task_scheduler: AsyncioFireAndForget,
    mock_cache_invalidator: AsyncMock,
):
    mock_sql_data_access.healthcheck.return_value = {"status": "ok"}
    mock_redis_storage.healthcheck.return_value = {"status": "ok"}

    dao = CachedFileMetaDataAccess(
        invalidator=mock_cache_invalidator,
        storage=mock_redis_storage,
        scheduler=task_scheduler,
        delegate=mock_sql_data_access,
        ttl=300,
    )

    result = await dao.healthcheck()

    assert result.get("status") == "ok"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_healthcheck_all_down(
    mock_sql_data_access: AsyncMock,
    mock_redis_storage: AsyncMock,
    task_scheduler: AsyncioFireAndForget,
    mock_cache_invalidator: AsyncMock,
):
    mock_sql_data_access.healthcheck.return_value = {"status": "down"}
    mock_redis_storage.healthcheck.return_value = {"status": "down"}

    dao = CachedFileMetaDataAccess(
        invalidator=mock_cache_invalidator,
        storage=mock_redis_storage,
        scheduler=task_scheduler,
        delegate=mock_sql_data_access,
        ttl=300,
    )

    result = await dao.healthcheck()

    assert result.get("status") == "down"


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_returns_none_and_skips_invalidation(
    mock_sql_data_access: AsyncMock,
    mock_redis_storage: AsyncMock,
    mock_cache_invalidator: AsyncMock,
    task_scheduler: AsyncioFireAndForget,
    filemeta: FileMeta,
):
    mock_sql_data_access.update.return_value = None

    dao = CachedFileMetaDataAccess(
        invalidator=mock_cache_invalidator,
        storage=mock_redis_storage,
        scheduler=task_scheduler,
        delegate=mock_sql_data_access,
        ttl=123,
    )

    result = await dao.update(filemeta)

    assert result is None
    mock_cache_invalidator.invalidate.assert_not_called()
