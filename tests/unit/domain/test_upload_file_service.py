import pytest
import asyncio
from shared.exceptions.domain import FilePolicyViolationEror, FileUploadFailedError
from domain.services.files.upload_file import UploadFileService
from tests.mocks.uow.base import FakeUoW
from tests.mocks.types.iterator import EmptyAsyncIterator, SimpleAsyncIterator


@pytest.mark.asyncio
async def test_succesful_upload(valid_filemeta, fake_stream):
    uow = FakeUoW()
    service = UploadFileService(uow)

    await service.execute(valid_filemeta, fake_stream)

    assert uow.committed is True
    assert uow.saved_meta == valid_filemeta


@pytest.mark.asyncio
async def test_disallowed_content_type_raises(
    fake_stream, invalid_content_type_filemeta
):
    uow = FakeUoW()
    service = UploadFileService(uow)

    with pytest.raises(FilePolicyViolationEror, match="Невалидный файл"):
        await service.execute(invalid_content_type_filemeta, fake_stream)


@pytest.mark.asyncio
async def test_infrastructure_error_triggers_rollback(fake_stream, valid_filemeta):
    uow = FakeUoW(fail=True)
    service = UploadFileService(uow)
    valid_filemeta
    with pytest.raises(FileUploadFailedError):
        await service.execute(valid_filemeta, fake_stream)

    assert uow.rolled_back is True
    assert uow.committed is False


@pytest.mark.asyncio
async def test_concurrent_file_upload(valid_filemeta):
    uow = FakeUoW()
    service = UploadFileService(uow)

    fake_stream_1 = SimpleAsyncIterator(b"file1-data")
    fake_stream_2 = SimpleAsyncIterator(b"file2-data")

    meta_1 = valid_filemeta
    meta_2 = valid_filemeta

    task1 = service.execute(meta_1, fake_stream_1)
    task2 = service.execute(meta_2, fake_stream_2)

    result_1, result_2 = await asyncio.gather(task1, task2)

    assert uow.committed
    assert not uow.rolled_back


@pytest.mark.asyncio
async def test_empty_stream_triggers_error(invalid_size_filemeta):
    uow = FakeUoW()
    service = UploadFileService(uow)
    empty_stream = EmptyAsyncIterator()
    invalid_size_filemeta

    with pytest.raises(FilePolicyViolationEror, match="Невалидный файл"):
        await service.execute(invalid_size_filemeta, empty_stream)


@pytest.mark.asyncio
async def test_file_meta_saved_properly(valid_filemeta, fake_stream):
    uow = FakeUoW()
    service = UploadFileService(uow)
    meta = valid_filemeta

    result = await service.execute(meta, fake_stream)

    assert result.id == meta.id
    assert result.name == meta.name
    assert result.content_type == meta.content_type
    assert result.size == meta.size
