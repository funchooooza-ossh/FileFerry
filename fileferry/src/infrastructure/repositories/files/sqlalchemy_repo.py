from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from contracts.application import FileRepository as FileRepositoryContract
from domain.models.dataclasses import FileMeta
from infrastructure.models.sqlalchemy.file import File
from infrastructure.utils.handlers.sqlalchemy_handler import wrap_sqlalchemy_failure
from shared.exceptions.infrastructure import RepositoryNotFoundError


class FileRepository(FileRepositoryContract):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @wrap_sqlalchemy_failure
    async def add(self, file_meta: FileMeta) -> None:
        file_model = File.from_domain(file_meta)
        self._session.add(file_model)
        await self._session.flush()

    @wrap_sqlalchemy_failure
    async def get(self, file_id: str) -> FileMeta:
        query = await self._session.execute(select(File).where(File.id == file_id))
        file_model = query.scalar_one_or_none()

        if file_model:
            return file_model.to_domain()
        raise RepositoryNotFoundError(f"File meta {file_id} not found")
