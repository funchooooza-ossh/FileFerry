from domain.models.dataclasses import FileMeta
from application.utils.upload_stream import file_to_iterator
from fastapi import UploadFile
from domain.services.files.upload_file import UploadFileService
from infrastructure.uow import SQLAlchemyMinioUnitOfWork
from miniopy_async import Minio
import uuid


class ApplicationFileService:
    @staticmethod
    async def create_file(name: str, file: UploadFile) -> FileMeta:
        client = Minio(
            endpoint="minio:9000",
            access_key="minioadmin",
            secret_key="miniosecret",
            secure=False,
        )
        uow = SQLAlchemyMinioUnitOfWork(client=client, bucket_name="default-bucket")
        service = UploadFileService(uow=uow)

        stream = file_to_iterator(file=file)
        file_id = uuid.uuid4().hex

        return await service.execute(file_id=file_id, file_name=name, data=stream)
