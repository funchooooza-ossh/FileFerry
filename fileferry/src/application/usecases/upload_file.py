from collections.abc import AsyncIterator

from application.utils.decorators import wrap_infrastructure_failures
from contracts.application import FilePolicy, FileStorage, UnitOfWork, UploadFileService
from domain.models.dataclasses import FileMeta


class UploadFileServiceImpl(UploadFileService):
    def __init__(
        self, uow: UnitOfWork, file_policy: FilePolicy, storage: FileStorage
    ) -> None:
        self._uow = uow
        self._policy = file_policy
        self._storage = storage

    @wrap_infrastructure_failures
    async def execute(self, meta: FileMeta, data: AsyncIterator[bytes]) -> FileMeta:
        self._policy.is_allowed(meta.content_type, meta.size)
        async with self._uow as uow:
            await uow.file_repo.add(meta)
            await self._storage.store(
                stream=data,
                file_id=meta.id.value,
                length=meta.size.value,
                content_type=meta.content_type.value,
            )
            await uow.commit()
        return meta
