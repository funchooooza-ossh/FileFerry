import pytest
from tests.mocks.uow.base import FakeUoW
from domain.models.dataclasses import FileMeta
from shared.exceptions.domain import FilePolicyViolationEror
from domain.services.files.upload_file import UploadFileService
from domain.models.enums import FileStatus


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

    with pytest.raises(FilePolicyViolationEror):
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
