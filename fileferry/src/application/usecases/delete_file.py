from application.utils.decorators import wrap_infrastructure_failures
from contracts.application import DeleteFileService, FileStorage, UnitOfWork
from domain.models.value_objects import FileId


class DeleteFileServiceImpl(DeleteFileService):
    def __init__(self, uow: UnitOfWork, storage: FileStorage) -> None:
        self._uow = uow
        self._storage = storage

    @wrap_infrastructure_failures
    async def execute(self, file_id: FileId) -> None:
        async with self._uow as uow:
            await uow.file_repo.delete(file_id=file_id.value)
            await self._storage.delete(file_id=file_id.value)

            await uow.commit()
