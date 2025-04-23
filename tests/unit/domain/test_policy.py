import pytest
from unittest.mock import MagicMock
from domain.models.value_objects import ContentType, FileSize
from domain.services.upload_policy import FilePolicyDefault
from shared.exceptions.domain import FilePolicyViolationEror


class FilePolicyExample(FilePolicyDefault):
    FORBIDDEN_TYPES = {"text/html", "application/x-empty", "application/javascript"}


@pytest.mark.asyncio
async def test_file_policy_allowed(valid_filemeta):
    content_type = valid_filemeta.content_type
    size = valid_filemeta.size

    result = FilePolicyExample.is_allowed(content_type, size)

    assert result is True


@pytest.mark.asyncio
async def test_file_policy_not_allowed_mime(invalid_content_type_filemeta):
    content_type = invalid_content_type_filemeta.content_type
    size = invalid_content_type_filemeta.size

    with pytest.raises(FilePolicyViolationEror, match="Невалидный файл"):
        result = FilePolicyExample.is_allowed(content_type, size)

        assert result is None


@pytest.mark.asyncio
async def test_file_policy_not_allowed_size():
    content_type = ContentType("application/pdf")
    size = MagicMock(spec=FileSize)
    size.value = 0

    with pytest.raises(FilePolicyViolationEror, match="Невалидный файл"):
        result = FilePolicyExample.is_allowed(content_type, size)

        assert result is None
