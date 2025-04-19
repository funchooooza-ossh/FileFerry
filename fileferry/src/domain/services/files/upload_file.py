from collections.abc import AsyncIterator

from domain.models.dataclasses import FileMeta
from domain.protocols import UnitOfWork
from domain.utility.file_policy import FilePolicy
from shared.exceptions.domain import FilePolicyViolationEror, FileUploadFailedError
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

        async with self._uow:
            try:
                await self._uow.save(meta=meta, stream=data)
            except InfrastructureError as exc:
                await self._uow.rollback()
                raise FileUploadFailedError("Не удалось загрузить файл") from exc
            else:
                await self._uow.commit()

                return meta
