from collections.abc import AsyncIterator
from unittest.mock import AsyncMock

import pytest
from application.usecases.files.upload import UploadUseCase
from domain.models import FileMeta
from shared.enums import Buckets
from shared.exceptions.application import DomainRejectedError


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
