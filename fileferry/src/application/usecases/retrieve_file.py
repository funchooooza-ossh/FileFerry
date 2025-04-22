from collections.abc import AsyncIterator

from contracts.application import FileStorage, RetrieveFileService, UnitOfWork
from domain.models.dataclasses import FileMeta
from domain.models.value_objects import FileId
from shared.exceptions.domain import FileRetrieveFailedError
from shared.exceptions.infrastructure import InfrastructureError


class RetrieveFileServiceImpl(RetrieveFileService):
    def __init__(self, uow: UnitOfWork, storage: FileStorage) -> None:
        self._uow = uow
        self._storage = storage

    async def execute(self, file_id: FileId) -> tuple[FileMeta, AsyncIterator[bytes]]:
        try:
            async with self._uow as uow:
                meta = await uow.file_repo.get(file_id=file_id.value)
                stream = await self._storage.retrieve(file_id=file_id.value)
                return meta, stream
        except InfrastructureError as exc:
            raise FileRetrieveFailedError("Ошибка получения файла") from exc
