from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from domain.models import FileMeta
from infrastructure.storage.minio import MiniOStorage
from miniopy_async.error import S3Error
from shared.enums import Buckets
from shared.exceptions.infrastructure import (
    AccessDeniedError,
    NoSuchBucketError,
    NoSuchKeyError,
    StorageError,
)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_miniostorage_upload(
    filemeta: FileMeta, stream: AsyncIterator[bytes], mock_minio_client: AsyncMock
):
    storage = MiniOStorage(mock_minio_client)

    await storage.upload(file_meta=filemeta, stream=stream, bucket=Buckets.DEFAULT)

    mock_minio_client.put_object.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_miniostorage_retrieve(
    filemeta: FileMeta, mock_minio_client: AsyncMock, chunks: list[bytes]
):
    storage = MiniOStorage(mock_minio_client)

    stream = await storage.retrieve(file_id=filemeta.get_id(), bucket=Buckets.DEFAULT)

    assert isinstance(stream, AsyncGenerator)

    collected: list[Any] = []
    async for chunk in stream:
        collected.append(chunk)

    assert collected == chunks
    mock_minio_client.get_object.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_miniostorage_delete(mock_minio_client: AsyncMock, filemeta: FileMeta):
    storage = MiniOStorage(mock_minio_client)

    await storage.delete(file_id=filemeta.get_id(), bucket=Buckets.DEFAULT)

    mock_minio_client.remove_object.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method_name, exception, expected_error, mock_method_name",
    [
        ("delete", S3Error, StorageError, "remove_object"),
        ("upload", S3Error, StorageError, "put_object"),
        (
            "delete",
            S3Error(
                code="AccessDenied",
                message="Access denied",
                resource="test_file",
                request_id="12345",
                host_id="host123",
                response=AsyncMock(),
                bucket_name="default-bucket",
                object_name="test_file",
            ),
            AccessDeniedError,
            "remove_object",
        ),
        (
            "delete",
            S3Error(
                code="NoSuchBucket",
                message="Bucket does not exist",
                resource="test_file",
                request_id="12345",
                host_id="host123",
                response=AsyncMock(),
                bucket_name="default-bucket",
                object_name="test_file",
            ),
            NoSuchBucketError,
            "remove_object",
        ),
        (
            "upload",
            S3Error(
                code="NoSuchKey",
                message="Key not found",
                resource="test_file",
                request_id="12345",
                host_id="host123",
                response=AsyncMock(),
                bucket_name="default-bucket",
                object_name="test_file",
            ),
            NoSuchKeyError,
            "put_object",
        ),
    ],
)
async def test_s3_error_mapping(
    method_name: str,
    exception: S3Error,
    expected_error: type[Exception],
    mock_method_name: str,
    mock_minio_client: AsyncMock,
    filemeta: FileMeta,
):
    if isinstance(exception, type):
        exc_instance = exception(
            code="UnknownError",
            message="Unknown S3 error",
            resource="test_file",
            request_id="12345",
            host_id="host123",
            response=AsyncMock(),
            bucket_name=Buckets.DEFAULT.value,
            object_name=filemeta.get_id(),
        )
    else:
        exc_instance = exception

    mocked_method = getattr(mock_minio_client, mock_method_name)
    mocked_method.side_effect = exc_instance

    storage = MiniOStorage(client=mock_minio_client)

    bucket = Buckets.DEFAULT
    data_stream = AsyncMock()

    with patch(
        "infrastructure.utils.stream_reader.AsyncStreamReader"
    ) as mock_stream_reader:
        mock_async_stream_reader = AsyncMock()
        mock_stream_reader.return_value = mock_async_stream_reader

        with pytest.raises(expected_error):
            if method_name == "delete":
                await storage.delete(file_id=filemeta.get_id(), bucket=bucket)
            elif method_name == "upload":
                await storage.upload(
                    file_meta=filemeta, stream=data_stream, bucket=bucket
                )

        mocked_method.assert_called_once()
