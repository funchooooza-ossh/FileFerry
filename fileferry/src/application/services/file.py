import uuid
from typing import AsyncIterator
from loguru import logger
from domain.models.dataclasses import FileMeta
from domain.protocols import UnitOfWork
from domain.models.enums import FileStatus
from domain.services.files.upload_file import UploadFileService
from shared.exceptions.domain import FilePolicyViolationEror
from shared.exceptions.application import (
    DomainRejectedError,
    StatusFailedError,
)
from application.di.uow.factory import UnitOfWorkFactory, KnownUoW
from infrastructure.utils.file_helper import FileHelper


class ApplicationFileService:
    """
    Единая точка входа в application-слой на создание файла.
    Принимает: name - имя файла, указанное юзером
               stream - Итератор байтов, чтоб не загружать файл в память целиком.
    Возвращает в случае успеха FileMeta - бизнес модель, либо ошибку.
    Параметр бэкенд - литерал, который предустанавливает известные конфигурации.
    Таким образом для тестов этого класса можно мокнуть фабрику UoW и все.
    """

    async def create_file(
        self,
        name: str,
        stream: AsyncIterator[bytes],
        *,
        backend: KnownUoW = "minio-sqla",
    ) -> FileMeta:
        file_id = uuid.uuid4().hex
        uow = self.get_uow(backend)
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
