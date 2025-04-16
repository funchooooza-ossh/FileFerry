import uuid
from miniopy_async import Minio
from typing import AsyncIterator
from domain.models.dataclasses import FileMeta
from domain.services.files.upload_file import UploadFileService
from infrastructure.uow import SQLAlchemyMinioUnitOfWork


class ApplicationFileService:
    @staticmethod
    async def create_file(name: str, stream: AsyncIterator[bytes]) -> FileMeta:
        client = Minio(
            endpoint="minio:9000",
            access_key="minioadmin",
            secret_key="miniosecret",
            secure=False,
        )
        uow = SQLAlchemyMinioUnitOfWork(client=client, bucket_name="default-bucket")
        service = UploadFileService(uow=uow)

        file_id = uuid.uuid4().hex

        return await service.execute(file_id=file_id, file_name=name, data=stream)
