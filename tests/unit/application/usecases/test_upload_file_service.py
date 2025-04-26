from unittest.mock import AsyncMock, MagicMock

import pytest
from application.usecases.upload_file import UploadFileServiceImpl
from domain.models.dataclasses import FileMeta
from domain.models.value_objects import ContentType, FileId, FileName, FileSize

from tests.helpers import aiter


@pytest.mark.asyncio
async def test_upload_success():
    file_id = FileId.new()
    file_meta = FileMeta(
        id=file_id,
        name=FileName("randname"),  # type: ignore
        size=FileSize(123),  # type: ignore
        content_type=ContentType("application/random"),  # type: ignore
    )
    stream = aiter([b"chunk", b"chunk2"])

    file_repo = AsyncMock()
    file_repo.add.return_value = file_meta

    uow_context = AsyncMock()
    uow_context.file_repo = file_repo

    uow = AsyncMock()
    uow.__aenter__.return_value = uow_context

    storage = AsyncMock()
    storage.store.return_value = None

    policy = MagicMock()
    policy.is_valid.return_value = True

    usecase = UploadFileServiceImpl(uow=uow, storage=storage, file_policy=policy)

    meta = await usecase.execute(meta=file_meta, data=stream)  # type: ignore

    assert isinstance(meta, FileMeta)
    file_repo.add.assert_awaited_once()
    storage.store.assert_awaited_once()
