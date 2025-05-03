from collections.abc import AsyncIterator, Callable
from typing import Optional

from contracts.application import UploadUseCaseContract
from contracts.domain import PolicyContract
from contracts.infrastructure import FileHelperContract, OperationCoordinationContract
from domain.models import FileMeta, FileName
from shared.enums import Buckets
from shared.exceptions.exc_classes.application import DomainRejectedError
from shared.exceptions.exc_classes.domain import FilePolicyViolationEror
from shared.exceptions.handlers.infra_handler import wrap_infrastructure_failures


class UploadUseCase(UploadUseCaseContract):
    def __init__(
        self,
        coordinator: OperationCoordinationContract,
        helper: FileHelperContract,
        policy: PolicyContract,
        meta_factory: Callable[[Optional[str], str, int, str], FileMeta],
    ) -> None:
        self._coordinator = coordinator
        self._helper = helper
        self._policy = policy
        self._meta_factory = meta_factory

    @wrap_infrastructure_failures
    async def execute(
        self, name: FileName, stream: AsyncIterator[bytes], bucket: Buckets
    ) -> FileMeta:
        stream, mime, size = await self._helper.analyze(stream=stream)
        file_meta = self._meta_factory(None, name.value, size, mime)
        try:
            self._policy.is_allowed(file_meta=file_meta)
        except FilePolicyViolationEror as exc:
            raise DomainRejectedError(message="Policy violation") from exc
        async with self._coordinator as transaction:
            await transaction.data_access.save(file_meta=file_meta)
            await transaction.file_storage.upload(
                file_meta=file_meta, stream=stream, bucket=bucket
            )

        return file_meta
