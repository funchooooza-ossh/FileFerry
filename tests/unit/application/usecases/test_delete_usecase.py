from unittest.mock import AsyncMock

import pytest
from application.usecases.files.delete import DeleteUseCase
from domain.models import FileId
from shared.enums import Buckets


@pytest.mark.asyncio
@pytest.mark.unit
async def test_delete_ok(
    fileid: FileId,
    mock_coordinator: AsyncMock,
):
    usecase = DeleteUseCase(coordinator=mock_coordinator)

    await usecase.execute(fileid, bucket=Buckets.DEFAULT)

    mock_coordinator.__aenter__.assert_called_once()
    mock_coordinator.__aexit__.assert_called_once_with(None, None, None)
    mock_coordinator.data_access.delete.assert_called_once_with(file_id=fileid.value)
    mock_coordinator.file_storage.delete.assert_called_once_with(
        file_id=fileid.value, bucket=Buckets.DEFAULT
    )
