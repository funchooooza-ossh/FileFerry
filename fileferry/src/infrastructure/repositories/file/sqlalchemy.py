from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.models.dataclasses import FileMeta
from infrastructure.models.sqlalchemy.file import File
from infrastructure.utils.handler import sqlalchemy_handle
from shared.exceptions.infrastructure import RepositoryNotFoundError


class FileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @sqlalchemy_handle
    async def add(self, file_meta: FileMeta) -> None:
        file_model = File.from_domain(file_meta)
        self._session.add(file_model)
        await self._session.flush()

    @sqlalchemy_handle
    async def get(self, file_id: str) -> FileMeta:
        query = await self._session.execute(select(File).filter(File.id == file_id))
        file_model = query.scalar_one_or_none()

        if file_model:
            return file_model.to_domain()
        raise RepositoryNotFoundError(f"File meta {file_id} not found")

    @sqlalchemy_handle
    async def commit(self) -> None:
        """
        НЕ ИСПОЛЬЗОВАТЬ НАПРЯМУЮ,
        ТОЛЬКО ДЛЯ КОНТЕКСТА UoW
        """
        await self._session.commit()

    @sqlalchemy_handle
    async def rollback(self) -> None:
        """
        НЕ ИСПОЛЬЗОВАТЬ НАПРЯМУЮ,
        ТОЛЬКО ДЛЯ КОНТЕКСТА UoW
        """
        await self._session.rollback()
