from collections.abc import AsyncIterator, Callable

from contracts.application import UploadUseCaseContract
from contracts.domain import PolicyContract
from contracts.infrastructure import AtomicOperationContract, FileHelperContract
from domain.models import FileMeta
from shared.enums import Buckets
from shared.exceptions.handlers.infra_hanlder import wrap_infrastructure_failures


class UploadUseCase(UploadUseCaseContract):
    def __init__(
        self,
        atomic: AtomicOperationContract,
        helper: FileHelperContract,
        policy: PolicyContract,
        meta_factory: Callable[[str, int, str], FileMeta],
    ) -> None:
        self._atomic = atomic
        self._helper = helper
        self._policy = policy
        self._meta_factory = meta_factory

    @wrap_infrastructure_failures
    async def execute(
        self, name: str, stream: AsyncIterator[bytes], bucket: Buckets
    ) -> FileMeta:
        stream, mime, size = await self._helper.analyze(stream=stream)
        file_meta = self._meta_factory(name, size, mime)
        self._policy.is_allowed(file_meta=file_meta)

        async with self._atomic as transaction:
            await transaction.data_access.save(file_meta=file_meta)
            await transaction.storage.upload(
                file_meta=file_meta, stream=stream, bucket=bucket
            )

        return file_meta
