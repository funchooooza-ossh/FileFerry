import uuid
from typing import AsyncIterator
from domain.models.dataclasses import FileMeta
from domain.models.enums import FileStatus
from domain.services.files.upload_file import UploadFileService
from infrastructure.uow import SQLAlchemyMinioUnitOfWork
from shared.exceptions.domain import FilePolicyViolationEror
from shared.exceptions.application import (
    DomainRejectedError,
    StatusFailedError,
)
from application.di.minio.factory import create_minio_client


class ApplicationFileService:
    @staticmethod
    async def create_file(
        name: str,
        stream: AsyncIterator[bytes],
    ) -> FileMeta:
        file_id = uuid.uuid4().hex
        client = create_minio_client(_type="default")
        uow = SQLAlchemyMinioUnitOfWork(client=client, bucket_name="default-bucket")
        service = UploadFileService(uow=uow)

        try:
            meta = await service.execute(
                file_id=file_id,
                file_name=name,
                data=stream,
            )

            if meta.status == FileStatus.FAILED:
                # Ошибка от domain, но причина может быть связана с инфраструктурой
                raise StatusFailedError(type=meta.reason)

            return meta

        except FilePolicyViolationEror as exc:
            # Нарушение бизнес-правил домена
            raise DomainRejectedError("File rejected due to domain rules") from exc
