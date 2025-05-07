from application.exceptions.infra_handler import wrap_infrastructure_failures
from contracts.application import DeleteUseCaseContract
from contracts.infrastructure import OperationCoordinationContract
from domain.models import FileId
from shared.enums import Buckets


class DeleteUseCase(DeleteUseCaseContract):
    def __init__(self, coordinator: OperationCoordinationContract) -> None:
        self._coordinator = coordinator

    @wrap_infrastructure_failures
    async def execute(self, file_id: FileId, bucket: Buckets) -> None:
        async with self._coordinator as transaction:
            await transaction.file_storage.delete(file_id=file_id.value, bucket=bucket)
            await transaction.data_access.delete(file_id=file_id.value)
