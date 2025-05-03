from contracts.application import DeleteUseCaseContract
from contracts.infrastructure import SQLAlchemyMinioCoordinationContract
from domain.models import FileId
from shared.enums import Buckets
from shared.exceptions.handlers.infra_handler import wrap_infrastructure_failures


class DeleteUseCase(DeleteUseCaseContract):
    def __init__(self, coordinator: SQLAlchemyMinioCoordinationContract) -> None:
        self._coordinator = coordinator

    @wrap_infrastructure_failures
    async def execute(self, file_id: FileId, bucket: Buckets) -> None:
        async with self._coordinator as transaction:
            await transaction.storage.delete(file_id=file_id.value, bucket=bucket)
            await transaction.db.delete(file_id=file_id.value)
