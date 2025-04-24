from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from types import TracebackType
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from contracts.application import UnitOfWork
from infrastructure.db.session import get_async_session
from infrastructure.repositories.files.sqlalchemy_repo import FileRepository
from infrastructure.utils.handlers.sqlalchemy_handler import wrap_sqlalchemy_failure


class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(
        self,
        session_factory: Callable[
            [], AbstractAsyncContextManager[AsyncSession]
        ] = get_async_session,
    ) -> None:
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self.file_repo: Optional[FileRepository]

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        self._session_ctx = self._session_factory()
        self._session = await self._session_ctx.__aenter__()

        self.file_repo = FileRepository(self._session)

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if hasattr(self, "_session_ctx"):
            await self._session_ctx.__aexit__(exc_type, exc_val, exc_tb)

    @wrap_sqlalchemy_failure
    async def commit(self) -> None:
        if self._session:
            await self._session.commit()

    @wrap_sqlalchemy_failure
    async def rollback(self) -> None:
        if self._session:
            await self._session.rollback()
