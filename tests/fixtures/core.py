import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from settings import settings


engine = create_async_engine(url=settings.DATABASE_URL)
async_session_maker = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession, autoflush=True
)


@pytest.fixture(scope="function")
async def session_factory() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
