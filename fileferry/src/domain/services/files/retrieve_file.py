from collections.abc import AsyncIterator

from application.protocols import RetrieveFileService
from domain.models.dataclasses import FileMeta
from domain.models.value_objects import FileId
from domain.protocols import UnitOfWork
from shared.exceptions.domain import FileRetrieveFailedError
from shared.exceptions.infrastructure import InfrastructureError


class RetrieveFileServiceImpl(RetrieveFileService):
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, file_id: FileId) -> tuple[FileMeta, AsyncIterator[bytes]]:
        try:
            async with self._uow as uow:
                meta, stream = await uow.retrieve(file_id=file_id)
                return meta, stream
        except InfrastructureError as exc:
            raise FileRetrieveFailedError("Ошибка получения файла") from exc
