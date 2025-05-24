from collections.abc import AsyncIterator
from unittest.mock import AsyncMock

import pytest
from contracts.infrastructure import FileHelperContract


@pytest.fixture
async def mock_filehelper(
    stream: AsyncIterator[bytes], valid_ctype: str, valid_filesize: int
) -> FileHelperContract:
    helper = AsyncMock()
    helper.analyze.return_value = (stream, valid_ctype, valid_filesize)
    return helper
