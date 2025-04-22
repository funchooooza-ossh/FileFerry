import pytest
import asyncio
from unittest.mock import MagicMock
from domain.services.upload_policy import FilePolicyDefault as FilePolicy
from domain.models.dataclasses import FileMeta
from domain.models.value_objects import FileId, FileName, ContentType, FileSize
from shared.exceptions.domain import FilePolicyViolationEror, FileUploadFailedError
from application.services.upload_file import UploadFileServiceImpl
from tests.mocks.uow.base import FakeUoW
from tests.mocks.types.iterator import EmptyAsyncIterator, SimpleAsyncIterator


@pytest.mark.asyncio
async def test_succesful_upload(valid_filemeta, fake_stream):
    uow = FakeUoW()
    policy = MagicMock()
    policy.is_allowed.return_value = True
    service = UploadFileServiceImpl(uow, policy)

    await service.execute(valid_filemeta, fake_stream)

    assert uow.committed is True
    assert uow.saved_meta == valid_filemeta


@pytest.mark.asyncio
async def test_disallowed_content_type_raises(
    fake_stream, invalid_content_type_filemeta
):
    uow = FakeUoW()
    policy = FilePolicy()
    service = UploadFileServiceImpl(uow, file_policy=policy)

    with pytest.raises(FilePolicyViolationEror, match="Невалидный файл"):
        await service.execute(invalid_content_type_filemeta, fake_stream)


@pytest.mark.asyncio
async def test_infrastructure_error_triggers_rollback(fake_stream, valid_filemeta):
    uow = FakeUoW(fail=True)
    policy = MagicMock()
    policy.is_allowed.return_value = True
    service = UploadFileServiceImpl(uow, file_policy=policy)
    valid_filemeta
    with pytest.raises(FileUploadFailedError):
        await service.execute(valid_filemeta, fake_stream)

    assert uow.rolled_back is True
    assert uow.committed is False


@pytest.mark.asyncio
async def test_concurrent_file_upload(valid_filemeta):
    uow = FakeUoW()
    policy = MagicMock()
    policy.is_allowed.return_value = True
    service = UploadFileServiceImpl(uow, file_policy=policy)

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
async def test_empty_stream_triggers_error():
    """
    Такого априори быть не может, ведь эта
    бинзес-модель создается через value objects
    и фабрику. но на всякий случай.
    """
    file_size = MagicMock(spec=FileSize)
    file_size.value = 0

    filemeta = FileMeta(
        id=FileId.new(),
        name=FileName(value="file"),
        size=file_size,
        content_type=ContentType(value="application/pdf"),
    )

    uow = FakeUoW()
    policy = FilePolicy()
    service = UploadFileServiceImpl(uow, policy)
    empty_stream = EmptyAsyncIterator()

    with pytest.raises(FilePolicyViolationEror, match="Невалидный файл"):
        await service.execute(filemeta, empty_stream)


@pytest.mark.asyncio
async def test_file_meta_saved_properly(valid_filemeta, fake_stream):
    uow = FakeUoW()
    policy = FilePolicy()
    service = UploadFileServiceImpl(uow, policy)
    meta = valid_filemeta

    result = await service.execute(meta, fake_stream)

    assert result.id == meta.id
    assert result.name == meta.name
    assert result.content_type == meta.content_type
    assert result.size == meta.size
