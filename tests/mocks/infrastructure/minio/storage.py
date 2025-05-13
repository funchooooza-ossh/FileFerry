from collections.abc import AsyncIterator
from unittest.mock import AsyncMock

import pytest
from infrastructure.storage.minio import MiniOStorage


@pytest.fixture(scope="session")
def mock_minio_storage(stream: AsyncIterator[bytes]) -> MiniOStorage:
    storage = AsyncMock()
    storage.upload = AsyncMock()
    storage.delete = AsyncMock()
    storage.healthcheck = AsyncMock()
    storage.retrieve = AsyncMock()
    storage.retrieve.return_value = stream
    return storage
