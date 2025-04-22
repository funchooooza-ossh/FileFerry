from collections.abc import AsyncGenerator
from types import TracebackType
from typing import Optional

from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from contracts.domain import UnitOfWork
from infrastructure.db.session import get_async_session
from infrastructure.repositories.files.minio import MinioRepository
from infrastructure.repositories.files.sqlalchemy import FileRepository
from infrastructure.utils.handler import sqlalchemy_handle


class SQLAlchemyMinioUnitOfWork(UnitOfWork):
    def __init__(
        self,
        client: Minio,
        bucket_name: str,
        session_factory: AsyncGenerator[AsyncSession, None] = get_async_session,
    ) -> None:
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self.file_repo: Optional[FileRepository] = None
        self.file_storage: Optional[MinioRepository] = None
        self.bucket_name = bucket_name
        self.client = client

    async def __aenter__(self) -> "SQLAlchemyMinioUnitOfWork":
        self._session_ctx = self._session_factory()
        self._session = await self._session_ctx.__aenter__()

        self.file_repo = FileRepository(self._session)
        self.file_storage = MinioRepository(self.client, self.bucket_name)

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
