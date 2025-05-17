from unittest.mock import AsyncMock

import pytest
from infrastructure.tasks.consistence import CacheInvalidator


@pytest.fixture(scope="function")
def mock_cache_invalidator() -> CacheInvalidator:
    invalidator = AsyncMock()
    return invalidator
