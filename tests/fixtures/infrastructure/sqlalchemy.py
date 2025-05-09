from collections.abc import AsyncGenerator

import pytest
from infrastructure.config.postgres import pg_settings
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


@pytest.fixture(scope="function")
async def async_engine() -> AsyncEngine:
    return create_async_engine(url=pg_settings.url)


@pytest.fixture(scope="function")
async def session(async_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    maker = async_sessionmaker(
        bind=async_engine, autoflush=False, expire_on_commit=False
    )
    async with maker() as session:
        yield session
