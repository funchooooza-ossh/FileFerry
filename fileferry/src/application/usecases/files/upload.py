from collections.abc import AsyncIterator, Callable
from typing import Optional

from application.exceptions.infra_handler import wrap_infrastructure_failures
from contracts.application import UploadUseCaseContract
from contracts.domain import PolicyContract
from contracts.infrastructure import FileHelperContract, OperationCoordinationContract
from domain.models import FileMeta, FileName
from shared.enums import Buckets
from shared.exceptions.application import DomainRejectedError
from shared.exceptions.domain import FilePolicyViolationError


class UploadUseCase(UploadUseCaseContract):
    """
    Класс UploadUseCase реализует сценарий загрузки файла с проверкой политики
    и сохранением метаданных файла.

    Атрибуты:
        coordinator (OperationCoordinationContract): Контракт для управления
            транзакциями и координацией операций.
        helper (FileHelperContract): Контракт для анализа и обработки файлов.
        policy (PolicyContract): Контракт для проверки политики загрузки файлов.
        meta_factory (Callable): Фабрика для создания объекта метаданных файла.

    Методы:
        execute(name, stream, bucket):
            Выполняет процесс загрузки файла, включая анализ, проверку политики,
            сохранение метаданных и загрузку файла в хранилище.
    """

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
        except FilePolicyViolationError as exc:
            raise DomainRejectedError(message="Policy violation") from exc
        async with self._coordinator as transaction:
            await transaction.data_access.save(file_meta=file_meta)
            await transaction.file_storage.upload(
                file_meta=file_meta, stream=stream, bucket=bucket
            )

        return file_meta
