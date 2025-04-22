from collections.abc import AsyncIterator

from contracts.api import UploadFileService
from contracts.application import FilePolicy, FileStorage, UnitOfWork
from domain.models.dataclasses import FileMeta
from shared.exceptions.domain import FileUploadFailedError
from shared.exceptions.infrastructure import InfrastructureError


class UploadFileServiceImpl(UploadFileService):
    def __init__(self, uow: UnitOfWork, file_policy: FilePolicy, storage: FileStorage) -> None:
        self._uow = uow
        self._policy = file_policy
        self._storage = storage

    async def execute(self, meta: FileMeta, data: AsyncIterator[bytes]) -> FileMeta:
        self._policy.is_allowed(meta.content_type, meta.size)

        async with self._uow as uow:
            try:
                await uow.file_repo.add(meta)
                await self._storage.store(
                    stream=data,
                    file_id=meta.id.value,
                    length=meta.size.value,
                    content_type=meta.content_type.value,
                )
            except InfrastructureError as exc:
                raise FileUploadFailedError("Не удалось загрузить файл") from exc

            await uow.commit()
            return meta
