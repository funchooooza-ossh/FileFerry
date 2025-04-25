from unittest.mock import AsyncMock

import pytest
from application.orchestrators.retrieve_file_adapter import RetrieveFileAPIAdapter
from domain.models.value_objects import FileId
from shared.exceptions.application import InvalidValueError

from tests.helpers import aiter, create_filemeta


@pytest.mark.asyncio
async def test_retrieve_success():
    file_id = FileId.new()
    file_meta = create_filemeta(file_id=file_id)
    stream = aiter([b"chunk1", b"chunk2"])
    retrieve_service = AsyncMock()
    retrieve_service.execute.return_value = (file_meta, stream)

    service = RetrieveFileAPIAdapter(retrieve_service=retrieve_service)

    meta, return_stream = await service.get(file_id=file_id.value)

    assert meta == file_meta
    assert stream == return_stream
    retrieve_service.execute.assert_called_once()


@pytest.mark.asyncio
async def test_retrieve_invalid_id():
    file_id = "erstdfj"
    retrieve_service = AsyncMock()

    service = RetrieveFileAPIAdapter(retrieve_service=retrieve_service)

    with pytest.raises(InvalidValueError, match="Невалидный id файла"):
        await service.get(file_id=file_id)
