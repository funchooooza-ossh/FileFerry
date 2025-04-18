from collections.abc import AsyncIterator

from loguru import logger

from domain.models.dataclasses import FileMeta
from domain.models.enums import FileStatus
from domain.protocols import UnitOfWork
from domain.utility.file_policy import FilePolicy
from shared.exceptions.domain import FilePolicyViolationEror
from shared.exceptions.infrastructure import InfrastructureError


class UploadFileService:
    """
    Блок бизнес-логики.
    Валидирует content-type входящего файла.
    Связан "контрактом" с протокольным UnitOfWork.
    В случае успешной валидации отдает команду на сохранение.
    Работает только с бизнес-моделью FileMeta.
    """

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, meta: FileMeta, data: AsyncIterator[bytes]) -> FileMeta:
        mime = FilePolicy.is_allowed(meta.content_type, meta.size)
        if not mime:
            raise FilePolicyViolationEror("Невалидный файл")
        meta.status = FileStatus.PENDING

        async with self._uow:
            try:
                await self._uow.save(meta=meta, stream=data)
            except InfrastructureError as exc:
                logger.warning(f"Infrasctructure error {exc}")
                await self._uow.rollback()
                meta.status = FileStatus.FAILED
                meta.reason = exc.type
                return meta
            else:
                await self._uow.commit()
                meta.status = FileStatus.STORED

                return meta
