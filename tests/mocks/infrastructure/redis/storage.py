from unittest.mock import AsyncMock

import pytest
from infrastructure.storage.redis import RedisFileMetaCacheStorage


@pytest.fixture(scope="function")
def mock_redis_storage() -> RedisFileMetaCacheStorage:
    storage = AsyncMock()
    return storage
