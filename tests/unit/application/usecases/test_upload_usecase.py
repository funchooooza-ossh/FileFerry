from collections.abc import AsyncIterator
from typing import Type
from unittest.mock import AsyncMock

import pytest
from application.exceptions.infra_handler import wrap_infrastructure_failures
from application.usecases.files.upload import UploadUseCase
from domain.models import FileMeta
from shared.enums import Buckets
from shared.exceptions.application import DomainRejectedError, FileOperationFailed
from shared.exceptions.infrastructure import (
    AccessDeniedError,
    EntityTooLargeError,
    InfraError,
    IntegrityError,
    InternalError,
    InvalidAccessKeyIdError,
    InvalidBucketNameError,
    NoResultFoundError,
    NoSuchBucketError,
    NoSuchKeyError,
    OperationalError,
    ProgrammingError,
)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_upload_ok(
    mock_coordinator: AsyncMock,
    mock_filehelper: AsyncMock,
    filepolicy_mock_true: AsyncMock,
    meta_factory_mock: AsyncMock,
    filemeta: FileMeta,
    stream: AsyncIterator[bytes],
):
    mock_coordinator.data_access.save.return_value = filemeta
    mock_filehelper.analyze.return_value = (
        stream,
        filemeta.get_content_type(),
        filemeta.get_size(),
    )
    usecase = UploadUseCase(
        coordinator=mock_coordinator,
        helper=mock_filehelper,
        policy=filepolicy_mock_true,
        meta_factory=meta_factory_mock,
    )

    result = await usecase.execute(
        name=filemeta._name,  # type: ignore
        stream=stream,
        bucket=Buckets.DEFAULT,
    )

    mock_filehelper.analyze.assert_called_once_with(stream=stream)
    filepolicy_mock_true.is_allowed.assert_called_once_with(file_meta=filemeta)
    mock_coordinator.__aenter__.assert_called_once()
    mock_coordinator.__aexit__.assert_called_once_with(None, None, None)
    mock_coordinator.data_access.save.assert_awaited_once_with(file_meta=filemeta)
    mock_coordinator.file_storage.upload.assert_awaited_once_with(
        file_meta=filemeta, stream=stream, bucket=Buckets.DEFAULT
    )

    assert result.get_id() == filemeta.get_id()
    assert result.get_content_type() == filemeta.get_content_type()
    assert result.get_name() == filemeta.get_name()
    assert result.get_size() == filemeta.get_size()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_upload_raises_domain_rejected_on_policy_violation(
    mock_coordinator: AsyncMock,
    mock_filehelper: AsyncMock,
    filepolicy_mock_raises_error: AsyncMock,
    meta_factory_mock: AsyncMock,
    filemeta: FileMeta,
    stream: AsyncIterator[bytes],
):
    mock_coordinator.data_access.save.return_value = filemeta
    mock_filehelper.analyze.return_value = (
        stream,
        filemeta.get_content_type(),
        filemeta.get_size(),
    )
    usecase = UploadUseCase(
        coordinator=mock_coordinator,
        helper=mock_filehelper,
        policy=filepolicy_mock_raises_error,
        meta_factory=meta_factory_mock,
    )
    with pytest.raises(DomainRejectedError, match="Policy violation"):
        await usecase.execute(
            name=filemeta._name,  # type: ignore
            stream=stream,
            bucket=Buckets.DEFAULT,
        )

        mock_filehelper.analyze.assert_called_once_with(stream=stream)
        filepolicy_mock_raises_error.is_allowed.assert_called_once_with(
            file_meta=filemeta
        )

        mock_coordinator.__aenter__.assert_not_called()
        mock_coordinator.__aexit__.assert_not_called()
        mock_coordinator.data_access.save.assert_not_called()
        mock_coordinator.file_storage.upload.assert_not_called()


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.parametrize(
    "exc_type, expected_status, expected_message_fragment",
    [
        (AccessDeniedError, 403, "Доступ к ресурсу был запрещен"),
        (NoSuchBucketError, 404, "Указанный бакет не существует"),
        (NoSuchKeyError, 404, "Указанный объект не найден в хранилище"),
        (InvalidAccessKeyIdError, 400, "Неверный идентификатор ключа доступа"),
        (EntityTooLargeError, 413, "Объект слишком большой для загрузки"),
        (InternalError, 500, "Внутренняя ошибка хранилища"),
        (InvalidBucketNameError, 400, "Неверное имя бакета"),
        (IntegrityError, 409, "Ошибка целостности данных в базе"),
        (NoResultFoundError, 404, "Результат не найден в базе данных"),
        (ProgrammingError, 400, "Ошибка в SQL-запросе или работе ORM"),
        (
            OperationalError,
            503,
            "Операционная ошибка при взаимодействии с базой данных",
        ),
    ],
)
async def test_wrap_infrastructure_failures_decorator_raises_mapped_domain_error(
    exc_type: Type[InfraError],
    expected_status: int,
    expected_message_fragment: str,
) -> None:
    @wrap_infrastructure_failures
    async def failing_function() -> None:
        raise exc_type()

    with pytest.raises(FileOperationFailed) as exc_info:
        await failing_function()

    exc = exc_info.value
    assert isinstance(exc, FileOperationFailed)
    assert exc.status_code == expected_status
    assert (
        expected_message_fragment in str(exc)
        or expected_message_fragment in exc.message  # type: ignore
    )
    assert exc.type == exc_type.__name__
