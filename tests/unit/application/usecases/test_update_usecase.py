# Перезапускаем окружение с нужными импортами
from typing import AsyncIterator
from unittest.mock import AsyncMock

import pytest
from application.usecases.files.update import UpdateUseCase
from domain.models import FileMeta
from shared.enums import Buckets
from shared.exceptions.application import (
    DomainRejectedError,
)


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_with_stream_and_successful_update(
    mock_coordinator: AsyncMock,
    mock_filehelper: AsyncMock,
    filepolicy_mock_true: AsyncMock,
    meta_factory_mock: AsyncMock,
    filemeta: FileMeta,
    stream: AsyncIterator[bytes],
):
    mock_filehelper.analyze.return_value = (
        stream,
        filemeta.get_content_type(),
        filemeta.get_size(),
    )
    mock_coordinator.data_access.update.return_value = filemeta

    usecase = UpdateUseCase(
        coordinator=mock_coordinator,
        helper=mock_filehelper,
        policy=filepolicy_mock_true,
        meta_factory=meta_factory_mock,
    )

    result = await usecase.execute(
        file_id=filemeta._id,  # type: ignore
        name=filemeta._name,  # type: ignore
        stream=stream,
        bucket=Buckets.DEFAULT,
    )

    assert result.get_id() == filemeta.get_id()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_with_stream_policy_violation(
    mock_coordinator: AsyncMock,
    mock_filehelper: AsyncMock,
    filepolicy_mock_raises_error: AsyncMock,
    meta_factory_mock: AsyncMock,
    filemeta: FileMeta,
    stream: AsyncIterator[bytes],
):
    mock_filehelper.analyze.return_value = (
        stream,
        filemeta.get_content_type(),
        filemeta.get_size(),
    )

    usecase = UpdateUseCase(
        coordinator=mock_coordinator,
        helper=mock_filehelper,
        policy=filepolicy_mock_raises_error,
        meta_factory=meta_factory_mock,
    )

    with pytest.raises(DomainRejectedError, match="Policy violation"):
        await usecase.execute(
            file_id=filemeta._id,  # type: ignore
            name=filemeta._name,  # type: ignore
            stream=stream,
            bucket=Buckets.DEFAULT,
        )


@pytest.mark.asyncio
@pytest.mark.unit
async def test_update_without_stream_successful_update(
    mock_coordinator: AsyncMock,
    mock_filehelper: AsyncMock,
    filepolicy_mock_true: AsyncMock,
    meta_factory_mock: AsyncMock,
    filemeta: FileMeta,
):
    mock_coordinator.data_access.get.return_value = filemeta
    mock_coordinator.data_access.update.return_value = filemeta

    usecase = UpdateUseCase(
        coordinator=mock_coordinator,
        helper=mock_filehelper,
        policy=filepolicy_mock_true,
        meta_factory=meta_factory_mock,
    )

    result = await usecase.execute(
        file_id=filemeta._id,  # type: ignore
        name=filemeta._name,  # type: ignore
        stream=None,
        bucket=Buckets.DEFAULT,
    )

    assert result.get_id() == filemeta.get_id()
