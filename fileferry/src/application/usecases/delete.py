from contracts.application import DeleteUseCaseContract
from contracts.infrastructure import SQLAlchemyMinioAtomicContract
from domain.models import FileId
from shared.enums import Buckets
from shared.exceptions.handlers.infra_handler import wrap_infrastructure_failures


class DeleteUseCase(DeleteUseCaseContract):
    def __init__(self, atomic: SQLAlchemyMinioAtomicContract) -> None:
        self._atomic = atomic

    @wrap_infrastructure_failures
    async def execute(self, file_id: FileId, bucket: Buckets) -> None:
        async with self._atomic as transaction:
            await transaction.storage.delete(file_id=file_id.value, bucket=bucket)
            await transaction.data_access.delete(file_id=file_id.value)
