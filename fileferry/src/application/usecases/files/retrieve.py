from collections.abc import AsyncIterator

from application.exceptions.infra_handler import wrap_infrastructure_failures
from contracts.application.usecases import RetrieveUseCaseContract
from contracts.infrastructure import OperationCoordinationContract
from domain.models import FileId, FileMeta
from shared.enums import Buckets


class RetrieveUseCase(RetrieveUseCaseContract):
    def __init__(self, coordinator: OperationCoordinationContract) -> None:
        self._coordinator = coordinator

    @wrap_infrastructure_failures
    async def execute(
        self, file_id: FileId, bucket: Buckets
    ) -> tuple[FileMeta, AsyncIterator[bytes]]:
        async with self._coordinator as transaction:
            meta = await transaction.data_access.get(
                file_id=file_id.value,
            )
            stream = await transaction.file_storage.retrieve(
                file_id=file_id.value, bucket=bucket
            )

        return meta, stream
