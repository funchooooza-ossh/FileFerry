import pytest
from unittest.mock import AsyncMock, MagicMock, Mock
from infrastructure.repositories.files.minio import MinioRepository
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


async def mock_chunk_generator():
    yield b"chunk1"
    yield b"chunk2"

async def mock_async_iterable():
    async for item in mock_chunk_generator():
        yield item




@pytest.mark.asyncio
async def test_retrieve_returns_chunks():
    mock_client = MagicMock()
    mock_client._client_session = Mock(return_value="fake_session")

    mock_content = MagicMock()
    mock_content.iter_chunked = Mock(return_value=mock_chunk_generator())

    mock_response = AsyncMock()
    mock_response.__aenter__.return_value = mock_response
    mock_response.__aexit__.return_value = None
    mock_response.content = mock_content

    mock_client.get_object = AsyncMock(return_value=mock_response)

    repo = MinioRepository(client=mock_client, bucket_name="test-bucket")

    stream = await repo.retrieve("some_file.txt")
    result = [chunk async for chunk in stream]

    assert result == [b"chunk1", b"chunk2"]
    mock_client._client_session.assert_called_once()
    mock_client.get_object.assert_awaited_once_with(
        bucket_name="test-bucket",
        object_name="some_file.txt",
        session="fake_session",
    )



@pytest.mark.asyncio
async def test_retrieve_raises_not_found_error():
    mock_client = MagicMock()
    mock_client._client_session = Mock(return_value="fake_session")

    mock_client.get_object = AsyncMock(side_effect=Exception("object does not exist"))

    repo = MinioRepository(client=mock_client, bucket_name="test-bucket")

    with pytest.raises(StorageNotFoundError) as exc_info:
        await repo.retrieve("missing_file.txt")

    assert "missing_file.txt" in str(exc_info.value)

    mock_client._client_session.assert_called_once()
    mock_client.get_object.assert_awaited_once_with(
        bucket_name="test-bucket",
        object_name="missing_file.txt",
        session="fake_session",
    )