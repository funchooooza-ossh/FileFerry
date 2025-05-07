from collections.abc import AsyncIterator, Callable
from typing import Optional

from application.exceptions.infra_handler import wrap_infrastructure_failures
from contracts.application import UpdateUseCaseContract
from contracts.domain import PolicyContract
from contracts.infrastructure import (
    FileHelperContract,
    OperationCoordinationContract,
)
from domain.models import FileId, FileMeta, FileName
from shared.enums import Buckets
from shared.exceptions.application import (
    ApplicationRunTimeError,
    DomainRejectedError,
)
from shared.exceptions.domain import FilePolicyViolationEror


class UpdateUseCase(UpdateUseCaseContract):
    def __init__(
        self,
        coordinator: OperationCoordinationContract,
        meta_factory: Callable[[Optional[str], str, int, str], FileMeta],
        helper: FileHelperContract,
        policy: PolicyContract,
    ) -> None:
        self._coordinator = coordinator
        self._meta_factory = meta_factory
        self._helper = helper
        self._policy = policy

    @wrap_infrastructure_failures
    async def execute(
        self,
        file_id: FileId,
        name: FileName,
        stream: Optional[AsyncIterator[bytes]],
        bucket: Buckets,
    ) -> FileMeta:
        analyzed = None
        meta = None

        if stream:
            analyzed = await self._helper.analyze(stream)
            stream, content_type, size = analyzed
            meta = self._meta_factory(file_id.value, name.value, size, content_type)
            try:
                self._policy.is_allowed(meta)
            except FilePolicyViolationEror as exc:
                raise DomainRejectedError(message="Policy violation") from exc

        async with self._coordinator as transaction:
            if meta and stream:
                await transaction.file_storage.upload(
                    file_meta=meta, stream=stream, bucket=bucket
                )
            else:
                meta = await transaction.data_access.get(file_id=file_id.value)
                meta = self._meta_factory(
                    file_id.value, name.value, meta.get_size(), meta.get_content_type()
                )
            meta = await transaction.data_access.update(meta=meta)
            if not meta:
                raise ApplicationRunTimeError(
                    "[CRITICAL] Logical error in update usecase. Meta is None"
                ) from None
            return meta
