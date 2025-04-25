from unittest.mock import AsyncMock, MagicMock

import pytest
from application.orchestrators.upload_file_adapter import UploadFileAPIAdapter
from shared.exceptions.application import DomainRejectedError
from shared.exceptions.domain import FilePolicyViolationEror

from tests.helpers import aiter, create_filemeta


@pytest.mark.asyncio
async def test_upload_success():
    analyzer = AsyncMock()
    stream = aiter([b"chunk1", "chunk2"])
    analyzer.analyze.return_value = stream, "application/pdf", 123
    meta = create_filemeta()
    meta_factory = MagicMock()
    meta_factory.return_value = meta
    upload_service = AsyncMock()
    upload_service.execute.return_value = meta

    adapter = UploadFileAPIAdapter(
        file_analyzer=analyzer, meta_factory=meta_factory, upload_service=upload_service
    )

    result = await adapter.create(name="test_name", stream=stream)  # type: ignore

    assert result == meta
    meta_factory.assert_called_once()
    upload_service.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_upload_policy_error():
    analyzer = AsyncMock()
    stream = aiter([b"chunk1", "chunk2"])
    analyzer.analyze.return_value = stream, "application/pdf", 123
    meta = create_filemeta()
    meta_factory = MagicMock()
    meta_factory.return_value = meta
    upload_service = AsyncMock()
    upload_service.execute.side_effect = FilePolicyViolationEror(
        "TEST POLICY VIOLATION"
    )

    adapter = UploadFileAPIAdapter(
        file_analyzer=analyzer, meta_factory=meta_factory, upload_service=upload_service
    )
    with pytest.raises(DomainRejectedError, match="File rejected by policy") as exc:
        await adapter.create(name="test_name", stream=stream)  # type: ignore

        meta_factory.assert_called_once()
        upload_service.execute.assert_awaited_once()
        assert exc.type == DomainRejectedError.__name__
