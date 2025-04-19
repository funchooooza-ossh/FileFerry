import pytest
from unittest.mock import AsyncMock
from infrastructure.repositories.file.minio import MinioRepository
from tests.helpers import aiter
from shared.exceptions.infrastructure import StorageError, StorageNotFoundError


@pytest.mark.asyncio
async def test_store_success(mocker):
    client = AsyncMock()
    repo = MinioRepository(client=client, bucket_name="test-bucket")

    await repo.store(
        file_id="abc-123",
        stream=aiter([b"file content"]),
        length=len(b"file content"),
        content_type="application/octet-stream",
    )

    client.put_object.assert_awaited_once()
    kwargs = client.put_object.call_args.kwargs
    assert kwargs["bucket_name"] == "test-bucket"
    assert kwargs["object_name"] == "abc-123"
    assert kwargs["length"] == len(b"file content")


@pytest.mark.asyncio
async def test_store_raises_storage_error(mocker):
    client = AsyncMock()
    client.put_object.side_effect = RuntimeError("boom")

    repo = MinioRepository(client, "some-bucket")

    with pytest.raises(StorageError) as err:
        await repo.store("file-id", aiter([b"1", b"2"]), 2, "application/pdf")

    assert "RuntimeError: boom" in str(err.value)


@pytest.mark.asyncio
async def test_retrieve_success(mocker):
    client = AsyncMock()
    response = AsyncMock()
    response.stream = lambda _: aiter([b"chunk1", b"chunk2"])
    client.get_object.return_value = response

    repo = MinioRepository(client, "my-bucket")

    result = []
    async for chunk in repo.retrieve("file123"):
        result.append(chunk)

    assert result == [b"chunk1", b"chunk2"]
    client.get_object.assert_awaited_once_with("my-bucket", "file123")


@pytest.mark.asyncio
async def test_retrieve_not_found(mocker):
    client = AsyncMock()
    client.get_object.side_effect = Exception("no such key")

    repo = MinioRepository(client, "bucket-x")

    with pytest.raises(StorageNotFoundError):
        async for _ in repo.retrieve("not-there"):
            pass
