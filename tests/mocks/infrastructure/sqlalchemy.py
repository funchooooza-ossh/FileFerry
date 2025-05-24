from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.add = AsyncMock()
    session.execute = AsyncMock()
    session.flush = AsyncMock()
    session.begin = AsyncMock()
    session.close = AsyncMock()
    return session
