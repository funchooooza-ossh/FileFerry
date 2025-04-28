from contracts.application import DeleteUseCaseContract
from contracts.infrastructure import SQLAlchemyMinioAtomicContract
from domain.models import FileId
from shared.enums import Buckets
from shared.exceptions.exc_classes.application import InvalidValueError
from shared.exceptions.handlers.infra_hanlder import wrap_infrastructure_failures


class DeleteUseCase(DeleteUseCaseContract):
    def __init__(self, atomic: SQLAlchemyMinioAtomicContract) -> None:
        self._atomic = atomic

    @wrap_infrastructure_failures
    async def execute(self, file_id: str, bucket: Buckets) -> None:
        try:
            FileId(file_id)
        except ValueError:
            raise InvalidValueError("Invalid file id") from None

        async with self._atomic as transaction:
            await transaction.storage.delete(file_id=file_id, bucket=bucket)
            await transaction.data_access.delete(file_id=file_id)
