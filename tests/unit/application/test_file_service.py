import pytest
from domain.models.dataclasses import FileMeta
from application.services.file import ApplicationFileService
from shared.exceptions.application import DomainRejectedError, StatusFailedError
from shared.exceptions.domain import FilePolicyViolationEror, FileUploadFailedError
from tests.helpers import aiter


@pytest.mark.asyncio
async def test_create_file_success(mocker):
    mock_uow = mocker.MagicMock()
    mock_upload_service = mocker.AsyncMock()
    mock_file = FileMeta(
        id="id",
        name="test.txt",
        content_type="text/plain",
        size=100,
    )

    mock_upload_service.return_value.execute.return_value = mock_file
    mocker.patch(
        "domain.services.files.upload_file.UploadFileService.execute",
        return_value=mock_upload_service.return_value,
    )
    mocker.patch(
        "application.services.file.ApplicationFileService.get_uow",
        return_value=mock_uow,
    )
    mocker.patch(
        "application.services.file.FileHelper.analyze",
        return_value=(aiter([b"data"]), "text/plain", 100),
    )

    result = await ApplicationFileService.create_file(
        name="test.txt", stream=aiter([b"data"])
    )
    assert result.id == "id"
    assert result.name == "test.txt"
    assert result.size == 100
    assert result.content_type == "text/plain"


@pytest.mark.asyncio
async def test_create_file_domain_violation(mocker):
    uow = mocker.AsyncMock()
    uow.save.side_effect = FilePolicyViolationEror()

    ApplicationFileService.get_uow = lambda _: uow

    with pytest.raises(DomainRejectedError) as err:
        await ApplicationFileService.create_file(
            name="virus.exe",
            stream=aiter([b"MZ..."]),
        )
    assert err.value.type == "FilePolicyViolationEror"


@pytest.mark.asyncio
async def test_create_file_failed_status(mocker, failed_filemeta):
    uow = mocker.AsyncMock()

    service_mock = mocker.patch(
        "application.services.file.UploadFileService",
        return_value=mocker.AsyncMock(
            execute=mocker.AsyncMock(side_effect=FileUploadFailedError),
        ),
    )
    mocker.patch.object(ApplicationFileService, "get_uow", return_value=uow)

    with pytest.raises(StatusFailedError) as exc_info:
        await ApplicationFileService.create_file(
            name="bad.pdf", stream=aiter([b"data"])
        )

    assert "Не удалось загрузить файл" in str(exc_info.value)
    assert exc_info.value.type == "FileUploadFailedError"
    service_mock.assert_called_once()


@pytest.mark.asyncio
async def test_create_file_unexpected_error(mocker):
    uow = mocker.AsyncMock()

    service_mock = mocker.patch(
        "application.services.file.UploadFileService",
        return_value=mocker.AsyncMock(
            execute=mocker.AsyncMock(side_effect=RuntimeError("unexpected error"))
        ),
    )

    mocker.patch.object(ApplicationFileService, "get_uow", return_value=uow)

    with pytest.raises(RuntimeError) as exc_info:
        await ApplicationFileService.create_file(
            name="x.pdf", stream=aiter([b"x-data"])
        )

    assert "unexpected error" in str(exc_info.value)
    service_mock.assert_called_once()
