from sqlalchemy.ext.asyncio import AsyncSession
from miniopy_async import Minio
from infrastructure.repositories.file.sqlalchemy import FileRepository
from infrastructure.repositories.file.minio import MinioRepository
from infrastructure.db.session import get_async_session
from typing import Optional, AsyncGenerator


class SQLAlchemyMinioUnitOfWork:
    def __init__(
        self,
        client: Minio,
        bucket_name: str,
        session_factory: AsyncGenerator[AsyncSession, None] = get_async_session,
    ):
        self._session_factory = session_factory
        self._session: Optional[AsyncSession] = None
        self.file_repo: Optional[FileRepository] = None
        self.file_storage: Optional[MinioRepository] = None
        self.bucket_name = bucket_name
        self.client = client

    async def __aenter__(self):
        self._session_ctx = self._session_factory()
        self._session = await self._session_ctx.__aenter__()

        self.file_repo = FileRepository(self._session)
        self.file_storage = MinioRepository(self.client, self.bucket_name)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, "_session_ctx"):
            await self._session_ctx.__aexit__(exc_type, exc_val, exc_tb)

    async def commit(self) -> None:
        """Выполнить commit для репозитория SQLAlchemy"""
        if self.file_repo:
            await self.file_repo.commit()

    async def rollback(self) -> None:
        """Выполнить rollback для репозитория SQLAlchemy"""
        if self.file_repo:
            await self.file_repo.rollback()
