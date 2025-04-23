import pytest
from typing import AsyncIterator


@pytest.fixture(scope="function")
async def fake_stream() -> AsyncIterator[bytes]:
    yield b"test-data"
