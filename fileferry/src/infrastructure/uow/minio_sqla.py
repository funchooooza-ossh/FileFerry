from collections.abc import AsyncGenerator, AsyncIterator
from types import TracebackType
from typing import Optional

from loguru import logger
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.dataclasses import FileMeta
from infrastructure.db.session import get_async_session
from infrastructure.repositories.file.minio import MinioRepository
from infrastructure.repositories.file.sqlalchemy import FileRepository
from shared.exceptions.infrastructure import InfrastructureError


class SQLAlchemyMinioUnitOfWork:
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

    async def save(self, meta: FileMeta, stream: AsyncIterator[bytes]) -> FileMeta:
        try:
            db_result = await self.file_repo.add(meta)
            await self.file_storage.store(
                file_id=meta.id.value,
                stream=stream,
                length=meta.size.value,
                content_type=meta.content_type.value,
            )
            return db_result
        except InfrastructureError as exc:
            raise exc
        except Exception as exc:
            logger.error(f"Unexpected error in save method: {exc!s}")
            raise InfrastructureError(str(exc)) from exc

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None:
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
