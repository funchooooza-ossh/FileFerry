import pytest
from unittest.mock import MagicMock, AsyncMock
from application.services.file import ApplicationFileServiceImpl
from shared.exceptions.application import DomainRejectedError, StatusFailedError
from shared.exceptions.domain import FilePolicyViolationEror, FileUploadFailedError


@pytest.mark.asyncio
async def test_create_file_success(valid_filemeta, fake_stream):
    file_analyzer = AsyncMock()
    file_analyzer.analyze.return_value = (
        fake_stream,
        valid_filemeta.content_type,
        valid_filemeta.size,
    )

    meta_factory = MagicMock()
    meta_factory.return_value = valid_filemeta

    upload_service = AsyncMock()
    upload_service.execute.return_value = valid_filemeta

    application = ApplicationFileServiceImpl(
        file_analyzer=file_analyzer,
        meta_factory=meta_factory,
        upload_service=upload_service,
    )

    result = await application.create(name=valid_filemeta.name, stream=fake_stream)

    assert result == valid_filemeta
    file_analyzer.analyze.assert_awaited_once()
    meta_factory.assert_called_once()
    upload_service.execute.assert_called_once()


@pytest.mark.asyncio
async def test_create_file_policy_violation(valid_filemeta, fake_stream):
    file_analyzer = AsyncMock()
    file_analyzer.analyze.return_value = (
        fake_stream,
        valid_filemeta.content_type,
        valid_filemeta.size,
    )

    meta_factory = MagicMock()
    meta_factory.return_value = valid_filemeta

    upload_service = AsyncMock()
    upload_service.execute.side_effect = FilePolicyViolationEror("Test")

    application = ApplicationFileServiceImpl(
        file_analyzer=file_analyzer,
        meta_factory=meta_factory,
        upload_service=upload_service,
    )

    with pytest.raises(DomainRejectedError, match="File rejected"):
        await application.create(name=valid_filemeta.name, stream=fake_stream)

    file_analyzer.analyze.assert_awaited_once()
    meta_factory.assert_called_once()
    upload_service.execute.assert_called_once()


@pytest.mark.asyncio
async def test_create_file_failed(valid_filemeta, fake_stream):
    file_analyzer = AsyncMock()
    file_analyzer.analyze.return_value = (
        fake_stream,
        valid_filemeta.content_type,
        valid_filemeta.size,
    )

    meta_factory = MagicMock()
    meta_factory.return_value = valid_filemeta

    upload_service = AsyncMock()
    upload_service.execute.side_effect = FileUploadFailedError("Test")

    application = ApplicationFileServiceImpl(
        file_analyzer=file_analyzer,
        meta_factory=meta_factory,
        upload_service=upload_service,
    )

    with pytest.raises(StatusFailedError, match="Upload failed"):
        await application.create(name=valid_filemeta.name, stream=fake_stream)

    file_analyzer.analyze.assert_awaited_once()
    meta_factory.assert_called_once()
    upload_service.execute.assert_called_once()
