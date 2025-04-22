from collections.abc import AsyncGenerator
from types import TracebackType
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from contracts.application import UnitOfWork
from infrastructure.db.session import get_async_session
from infrastructure.repositories.files.sqlalchemy import FileRepository
from infrastructure.utils.handler import sqlalchemy_handle


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(
        self,
        session_factory: AsyncGenerator[AsyncSession, None] = get_async_session,
    ) -> None:
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self.file_repo: Optional[FileRepository] = None

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        self._session_ctx = self._session_factory()
        self._session = await self._session_ctx.__aenter__()

        self.file_repo = FileRepository(self._session)

        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
        if hasattr(self, "_session_ctx"):
            await self._session_ctx.__aexit__(exc_type, exc_val, exc_tb)

    @sqlalchemy_handle
    async def commit(self) -> None:
        await self._session.commit()

    @sqlalchemy_handle
    async def rollback(self) -> None:
        await self._session.rollback()
