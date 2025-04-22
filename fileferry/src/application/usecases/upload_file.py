from collections.abc import AsyncIterator

from contracts.application import FilePolicy, FileStorage, UnitOfWork, UploadFileService
from domain.models.dataclasses import FileMeta
from shared.exceptions.domain import FileUploadFailedError
from shared.exceptions.infrastructure import InfrastructureError, NoSuchBucketError


class UploadFileServiceImpl(UploadFileService):
    def __init__(self, uow: UnitOfWork, file_policy: FilePolicy, storage: FileStorage) -> None:
        self._uow = uow
        self._policy = file_policy
        self._storage = storage

    async def execute(self, meta: FileMeta, data: AsyncIterator[bytes]) -> FileMeta:
        self._policy.is_allowed(meta.content_type, meta.size)
        try:
            async with self._uow as uow:
                await uow.file_repo.add(meta)
            await self._storage.store(
                stream=data,
                file_id=meta.id.value,
                length=meta.size.value,
                content_type=meta.content_type.value,
            )
        except NoSuchBucketError as exc:
            raise FileUploadFailedError("Запрошенный ресурс не существует") from exc
        except InfrastructureError as exc:
            raise FileUploadFailedError("Не удалось загрузить файл") from exc
        else:
            await uow.commit()
            return meta
