from collections.abc import AsyncIterator

from application.utils.decorators import wrap_infrastructure_failures
from contracts.application import FileStorage, RetrieveFileService, UnitOfWork
from domain.models.dataclasses import FileMeta
from domain.models.value_objects import FileId
from infrastructure.config.minio import ExistingBuckets


class RetrieveFileServiceImpl(RetrieveFileService):
    def __init__(self, uow: UnitOfWork, storage: FileStorage) -> None:
        self._uow = uow
        self._storage = storage

    @wrap_infrastructure_failures
    async def execute(
        self, file_id: FileId, bucket: ExistingBuckets
    ) -> tuple[FileMeta, AsyncIterator[bytes]]:
        async with self._uow as uow:
            meta = await uow.file_repo.get(file_id=file_id.value)
            stream = await self._storage.retrieve(file_id=file_id.value, bucket=bucket)

        return meta, stream
