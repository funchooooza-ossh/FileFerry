from typing import AsyncIterator
from loguru import logger
from domain.models.dataclasses import FileMeta
from domain.models.enums import FileStatus
from domain.protocols import UnitOfWork
from domain.utility.file_policy import FilePolicy
from domain.utility.file_helper import FileHelper
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

    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(
        self, file_id: str, file_name: str, data: AsyncIterator[bytes]
    ) -> FileMeta:
        stream = FileHelper.iterator_to_peekable_stream(data)
        header = await FileHelper.get_stream_header(stream)
        mime = FileHelper.detect_mime(header)
        size = await FileHelper.get_stream_size(stream)

        mime = FilePolicy.is_allowed(mime)
        if not mime:
            raise FilePolicyViolationEror("Невалидный файл")

        meta = FileMeta(
            id=file_id,
            size=size,
            content_type=mime,
            name=file_name,
            status=FileStatus.PENDING,
        )

        async with self._uow:
            try:
                await self._uow.file_repo.add(meta)
                await self._uow.file_storage.store(
                    file_id=file_id,
                    stream=stream.iter(),
                    length=size,
                    content_type=mime,
                )
            except InfrastructureError as exc:
                logger.warning(exc)
                await self._uow.rollback()
                meta.status = FileStatus.FAILED
                meta.reason = exc.type
                return meta
            else:
                await self._uow.commit()
                meta.status = FileStatus.STORED

                return meta
