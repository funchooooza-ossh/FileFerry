from collections.abc import AsyncIterator
from unittest.mock import AsyncMock

import pytest
from application.usecases.files.retrieve import RetrieveUseCase
from domain.models import FileId, FileMeta
from shared.enums import Buckets


@pytest.mark.asyncio
@pytest.mark.unit
async def test_retrieve_ok(
    mock_coordinator: AsyncMock,
    fileid: FileId,
    filemeta: FileMeta,
    stream: AsyncIterator[bytes],
):
    cord = mock_coordinator
    cord.data_access.get.return_value = filemeta
    cord.file_storage.retrieve.return_value = stream

    usecase = RetrieveUseCase(coordinator=cord)

    meta, returned_stream = await usecase.execute(fileid, bucket=Buckets.DEFAULT)

    cord.data_access.get.assert_called_once_with(file_id=fileid.value)
    cord.file_storage.retrieve.assert_called_once_with(
        file_id=fileid.value, bucket=Buckets.DEFAULT
    )
    assert meta.get_id() == filemeta.get_id()
    assert meta.get_name() == filemeta.get_name()
    assert meta.get_size() == filemeta.get_size()
    assert meta.get_content_type() == filemeta.get_content_type()

    assert returned_stream == stream
