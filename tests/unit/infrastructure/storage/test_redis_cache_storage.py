from typing import Optional
from unittest.mock import AsyncMock, patch

import pytest
from domain.models import FileMeta
from infrastructure.storage.redis import RedisFileMetaCacheStorage
from infrastructure.types.health.component_health import ComponentStatus
from redis.exceptions import ConnectionError, RedisError, TimeoutError


@pytest.mark.unit
@pytest.mark.asyncio
async def test_cache_get(
    mock_redis_client: AsyncMock,
    cache_prefix: str,
    filemeta_bytes: bytes,
    filemeta: FileMeta,
):
    client = mock_redis_client
    client.get.return_value = filemeta_bytes
    storage = RedisFileMetaCacheStorage(client=client, prefix=cache_prefix)

    cached_meta = await storage.get(filemeta.get_id())

    assert cached_meta
    assert cached_meta.get_id() == filemeta.get_id()
    assert cached_meta.get_name() == filemeta.get_name()
    assert cached_meta.get_size() == filemeta.get_size()
    assert cached_meta.get_content_type() == filemeta.get_content_type()

    client.get.assert_awaited_once_with(f"{cache_prefix}:{filemeta.get_id()}")


@pytest.mark.unit
@pytest.mark.asyncio
async def test_cache_set(
    mock_redis_client: AsyncMock,
    cache_prefix: str,
    filemeta_string: str,
    filemeta: FileMeta,
):
    client = mock_redis_client
    storage = RedisFileMetaCacheStorage(client=client, prefix=cache_prefix)
    ttl = 300

    await storage.set(meta=filemeta, ttl=ttl)

    client.set.assert_called_once_with(
        name=f"{cache_prefix}:{filemeta.get_id()}", value=filemeta_string, ex=ttl
    )


@pytest.mark.unit
@pytest.mark.asyncio
async def test_cache_delete(
    mock_redis_client: AsyncMock,
    cache_prefix: str,
    filemeta: FileMeta,
):
    client = mock_redis_client
    storage = RedisFileMetaCacheStorage(client=client, prefix=cache_prefix)

    await storage.delete(filemeta.get_id())

    client.delete.assert_awaited_once_with(f"{cache_prefix}:{filemeta.get_id()}")


@pytest.mark.unit
def test_cache_serialize_and_deserialize(
    mock_redis_client: AsyncMock,
    cache_prefix: str,
    filemeta: FileMeta,
    filemeta_string: str,
    filemeta_bytes: bytes,
):
    """BTW Redis encoding strings by itself"""
    client = mock_redis_client
    storage = RedisFileMetaCacheStorage(client=client, prefix=cache_prefix)

    serialized = storage.serialize_meta(filemeta)
    deserialized = storage.deserialize_meta(filemeta_bytes)

    assert deserialized == filemeta
    assert serialized == filemeta_string


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception, expected_result, expected_log_part",
    [
        (
            None,
            None,
            "[REDIS][OK]",
        ),
        (ConnectionError("conn down"), None, "[REDIS][ERR][GET]"),
        (TimeoutError("timeout"), None, "[REDIS][ERR][GET]"),
        (RedisError("bad redis"), None, "[REDIS][ERR][GET]"),
    ],
)
async def test_redis_get_with_wrapper(
    cache_prefix: str,
    expected_log_part: str,
    mock_redis_client: AsyncMock,
    filemeta: FileMeta,
    filemeta_bytes: bytes,
    caplog: pytest.LogCaptureFixture,
    exception: Optional[type[Exception]],
    expected_result: Optional[FileMeta],
):
    storage = RedisFileMetaCacheStorage(client=mock_redis_client, prefix=cache_prefix)

    file_id = filemeta.get_id()
    if exception is None:
        raw_value = filemeta_bytes
        expected_result = filemeta
        mock_redis_client.get.return_value = raw_value
        storage.deserialize_meta = lambda raw: filemeta
    else:
        mock_redis_client.get.side_effect = exception

    with caplog.at_level("WARNING" if exception else "INFO"):
        result = await storage.get(file_id)

    assert result == expected_result
    assert any(expected_log_part in rec.message for rec in caplog.records)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception, expected_exception, expected_log_part",
    [
        (
            ConnectionError("connection failed"),
            ConnectionError,
            "[REDIS][ERR][DELETE]",
        ),
        (
            TimeoutError("timeout occurred"),
            TimeoutError,
            "[REDIS][ERR][DELETE]",
        ),
        (
            RedisError("redis is down"),
            RedisError,
            "[REDIS][ERR][DELETE]",
        ),
    ],
)
async def test_redis_delete_with_raising(
    mock_redis_client: AsyncMock,
    caplog: pytest.LogCaptureFixture,
    cache_prefix: str,
    filemeta: FileMeta,
    exception: Exception,
    expected_exception: type[Exception],
    expected_log_part: str,
):
    storage = RedisFileMetaCacheStorage(client=mock_redis_client, prefix=cache_prefix)
    file_id = filemeta.get_id()
    key = f"{cache_prefix}:{file_id}"
    mock_redis_client.delete.side_effect = exception

    with caplog.at_level("WARNING"), pytest.raises(expected_exception):
        await storage.delete(file_id)

    # Проверка лога
    assert any(
        expected_log_part.replace("fileid", file_id) in rec.message
        for rec in caplog.records
    )

    # Проверка вызова метода Redis
    mock_redis_client.delete.assert_called_once_with(key)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "ping_result, info_result, latency, exception, expected_status, expected_error, expected_version",
    [
        (True, {"redis_version": "7.0.11"}, 0.005, None, "ok", None, "Redis 7.0.11"),
        (
            True,
            {"redis_version": "7.0.11"},
            0.030,
            None,
            "degraded",
            None,
            "Redis 7.0.11",
        ),
        (
            False,
            {"redis_version": "7.0.11"},
            0.005,
            None,
            "degraded",
            "no pong from redis",
            None,
        ),
        (None, None, 0.005, RedisError("redis dead"), "down", "redis dead", None),
    ],
)
async def test_redis_healthcheck(
    ping_result: bool | None,
    info_result: dict[str, str] | None,
    latency: float,
    exception: Exception | None,
    expected_status: str,
    expected_error: str | None,
    expected_version: str | None,
    mock_redis_client: AsyncMock,
    cache_prefix: str,
):
    storage = RedisFileMetaCacheStorage(client=mock_redis_client, prefix=cache_prefix)

    if exception:
        mock_redis_client.ping.side_effect = exception
        mock_redis_client.info.side_effect = exception
    else:
        mock_redis_client.ping.return_value = ping_result
        mock_redis_client.info.return_value = info_result or {}

    with patch("time.perf_counter", side_effect=[0.0, latency]):
        result: ComponentStatus = await storage.healthcheck()

    assert result.get("status") == expected_status

    if expected_error:
        assert result.get("error") == expected_error
    else:
        assert result.get("latency_ms") == pytest.approx(latency * 1000, rel=0.1)  # type: ignore
        assert result.get("details") is not None
        if expected_version:
            assert result.get("details", {}).get("version_raw") == expected_version
