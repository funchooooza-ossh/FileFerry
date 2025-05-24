from unittest.mock import AsyncMock

import pytest
from redis.asyncio import Redis


@pytest.fixture(scope="function")
def mock_redis_client() -> Redis:
    client = AsyncMock()
    client.get = AsyncMock()
    client.set = AsyncMock()
    client.delete = AsyncMock()
    return client
