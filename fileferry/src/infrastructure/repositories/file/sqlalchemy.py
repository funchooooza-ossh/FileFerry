from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from infrastructure.models.sqlalchemy.file import File
from shared.exceptions.infrastructure import RepositoryNotFoundError
from domain.models.dataclasses import FileMeta


class FileRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, file_meta: FileMeta) -> None:
        file_model = File.from_domain(file_meta)
        self._session.add(file_model)
        await self._session.flush()

    async def get(self, file_id: str) -> FileMeta:
        query = await self._session.execute(select(File).filter(File.id == file_id))
        file_model = query.scalar_one_or_none()

        if file_model:
            return file_model.to_domain()
        raise RepositoryNotFoundError(f"File meta {file_id} not found")

    async def commit(self) -> None:
        """
        НЕ ИСПОЛЬЗОВАТЬ НАПРЯМУЮ,
        ТОЛЬКО ДЛЯ КОНТЕКСТА UoW
        """
        await self._session.commit()

    async def rollback(self) -> None:
        """
        НЕ ИСПОЛЬЗОВАТЬ НАПРЯМУЮ,
        ТОЛЬКО ДЛЯ КОНТЕКСТА UoW
        """
        await self._session.rollback()
