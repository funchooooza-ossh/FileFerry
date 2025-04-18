import uuid
from collections.abc import AsyncIterator

from loguru import logger

from application.di.uow.factory import KnownUoW, UnitOfWorkFactory
from domain.models.dataclasses import FileMeta
from domain.models.enums import FileStatus
from domain.protocols import UnitOfWork
from domain.services.files.upload_file import UploadFileService
from infrastructure.utils.file_helper import FileHelper
from shared.exceptions.application import (
    DomainRejectedError,
    StatusFailedError,
)
from shared.exceptions.domain import FilePolicyViolationEror


class ApplicationFileService:
    """
    Единая точка входа в application-слой на создание файла.
    Принимает: name - имя файла, указанное юзером
               stream - Итератор байтов, чтоб не загружать файл в память целиком.
    Возвращает в случае успеха FileMeta - бизнес модель, либо ошибку.
    Параметр бэкенд - литерал, который предустанавливает известные конфигурации.
    Таким образом для тестов этого класса можно мокнуть фабрику UoW и все.
    """

    @classmethod
    async def create_file(
        cls,
        name: str,
        stream: AsyncIterator[bytes],
        *,
        backend: KnownUoW = "minio-sqla",
    ) -> FileMeta:
        file_id = uuid.uuid4().hex
        uow = cls.get_uow(backend)
        service = UploadFileService(uow=uow)

        stream, mime, size = await FileHelper.analyze(stream)
        meta = FileMeta(
            id=file_id, name=name, content_type=mime, size=size, status=None
        )

        try:
            meta = await service.execute(
                meta=meta,
                data=stream,
            )

            if meta.status == FileStatus.FAILED:
                # Ошибка от domain, но причина может быть связана с инфраструктурой
                logger.warning(f"File upload failed: {meta.reason}")
                raise StatusFailedError(message="Operation failed", type=meta.reason)
            return meta

        except FilePolicyViolationEror as exc:
            # Нарушение бизнес-правил домена
            raise DomainRejectedError(
                message="File rejected due to domain rules", type=exc.type
            ) from exc

    @staticmethod
    def get_uow(config: KnownUoW) -> UnitOfWork:
        return UnitOfWorkFactory.create(config=config)
