import pytest
import asyncio
from domain.models.dataclasses import FileMeta
from shared.exceptions.domain import FilePolicyViolationEror
from domain.services.files.upload_file import UploadFileService
from domain.models.enums import FileStatus
from tests.mocks.uow.base import FakeUoW
from tests.mocks.types.iterator import EmptyAsyncIterator, SimpleAsyncIterator


@pytest.mark.asyncio
async def test_succesful_upload(fake_stream):
    uow = FakeUoW()
    service = UploadFileService(uow)
    meta = FileMeta(
        id="some id", name="test.txt", content_type="text/plain", size=123, status=None
    )

    result = await service.execute(meta, fake_stream)

    assert result.status == FileStatus.STORED
    assert uow.committed is True
    assert uow.saved_meta == meta


@pytest.mark.asyncio
async def test_disallowed_content_type_raises(fake_stream):
    uow = FakeUoW()
    service = UploadFileService(uow)
    meta = FileMeta(
        id="2",
        name="evil.js",
        content_type="application/javascript",
        size=456,
        status=None,
    )

    with pytest.raises(FilePolicyViolationEror, match="Невалидный файл"):
        await service.execute(meta, fake_stream)


@pytest.mark.asyncio
async def test_infrastructure_error_triggers_rollback(fake_stream):
    uow = FakeUoW(fail=True)
    service = UploadFileService(uow)
    meta = FileMeta(
        id="3", name="fail.pdf", content_type="application/pdf", size=789, status=None
    )

    result = await service.execute(meta, fake_stream)

    assert result.status == FileStatus.FAILED
    assert result.reason == "InfrastructureError"
    assert uow.rolled_back is True
    assert uow.committed is False


@pytest.mark.asyncio
async def test_concurrent_file_upload():
    uow = FakeUoW()
    service = UploadFileService(uow)

    fake_stream_1 = SimpleAsyncIterator(b"file1-data")
    fake_stream_2 = SimpleAsyncIterator(b"file2-data")

    meta_1 = FileMeta(
        id="6", name="file1.pdf", content_type="application/pdf", size=123, status=None
    )
    meta_2 = FileMeta(
        id="7", name="file2.pdf", content_type="application/pdf", size=456, status=None
    )

    task1 = service.execute(meta_1, fake_stream_1)
    task2 = service.execute(meta_2, fake_stream_2)

    result_1, result_2 = await asyncio.gather(task1, task2)

    assert result_1.status == FileStatus.STORED
    assert result_2.status == FileStatus.STORED


@pytest.mark.asyncio
async def test_empty_stream_triggers_error():
    uow = FakeUoW()
    service = UploadFileService(uow)
    empty_stream = EmptyAsyncIterator()
    meta = FileMeta(
        id="5", name="empty.pdf", content_type="application/pdf", size=0, status=None
    )

    with pytest.raises(FilePolicyViolationEror, match="Невалидный файл"):
        await service.execute(meta, empty_stream)


@pytest.mark.asyncio
async def test_file_meta_saved_properly(fake_stream):
    uow = FakeUoW()
    service = UploadFileService(uow)
    meta = FileMeta(
        id="9", name="test.pdf", content_type="application/pdf", size=456, status=None
    )

    result = await service.execute(meta, fake_stream)

    assert result.id == meta.id
    assert result.name == meta.name
    assert result.content_type == meta.content_type
    assert result.status == FileStatus.STORED
    assert result.size == meta.size
