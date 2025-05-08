from collections.abc import AsyncIterator
from typing import Optional

from loguru import logger

from contracts.application import (
    ApplicationAdapterContract,
    DeleteUseCaseContract,
    RetrieveUseCaseContract,
    UpdateUseCaseContract,
    UploadUseCaseContract,
)
from domain.models import FileId, FileMeta, FileName
from shared.enums import Buckets
from shared.exceptions.application import ApplicationRunTimeError

logger = logger.bind(name="info")


class FileApplicationAdapter(ApplicationAdapterContract):
    """
    FileApplicationAdapter — это адаптер для операций с файлами, который реализует доступ
    к CRUD-операциям через необходимые use case. Он предоставляет методы для загрузки,
    получения, удаления и обновления файлов.
    Атрибуты:
        _upload_usecase (Optional[UploadUseCaseContract]): Use case для обработки загрузки файлов.
        _retrieve_usecase (Optional[RetrieveUseCaseContract]): Use case для получения файлов.
        _delete_usecase (Optional[DeleteUseCaseContract]): Use case для удаления файлов.
        _update_usecase (Optional[UpdateUseCaseContract]): Use case для обновления файлов.
    Методы:
        upload(name: FileName, stream: AsyncIterator[bytes], bucket: Buckets) -> FileMeta:
            Загружает файл в указанный bucket. Вызывает ApplicationRunTimeError, если
            use case для загрузки недоступен.
        retrieve(file_id: FileId, bucket: Buckets) -> tuple[FileMeta, AsyncIterator[bytes]]:
            Получает файл и его метаданные из указанного bucket. Вызывает
            ApplicationRunTimeError, если use case для получения недоступен.
        delete(file_id: FileId, bucket: Buckets) -> None:
            Удаляет файл из указанного bucket. Вызывает ApplicationRunTimeError, если
            use case для удаления недоступен.
        update(bucket: Buckets, file_id: FileId, name: FileName, stream: Optional[AsyncIterator[bytes]] = None) -> FileMeta:
            Обновляет метаданные файла и, при необходимости, его содержимое в указанном bucket.
            Вызывает ApplicationRunTimeError, если use case для обновления недоступен.
    """

    def __init__(
        self,
        upload_usecase: Optional[UploadUseCaseContract] = None,
        retrieve_usecase: Optional[RetrieveUseCaseContract] = None,
        delete_usecase: Optional[DeleteUseCaseContract] = None,
        update_usecase: Optional[UpdateUseCaseContract] = None,
    ) -> None:
        self._upload_usecase = upload_usecase
        self._retrieve_usecase = retrieve_usecase
        self._delete_usecase = delete_usecase
        self._update_usecase = update_usecase

    async def upload(
        self,
        *,
        name: FileName,
        stream: AsyncIterator[bytes],
        bucket: Buckets,
    ) -> FileMeta:
        if not self._upload_usecase:
            raise ApplicationRunTimeError("Upload usecase is not available")
        meta = await self._upload_usecase.execute(
            name=name,
            stream=stream,
            bucket=bucket,
        )
        logger.info(f"[APP] File uploaded: id={meta.get_id()}, size={meta.get_size()}")
        return meta

    async def retrieve(
        self,
        *,
        file_id: FileId,
        bucket: Buckets,
    ) -> tuple[FileMeta, AsyncIterator[bytes]]:
        if not self._retrieve_usecase:
            raise ApplicationRunTimeError("Retrieve usecase is not available")

        meta, stream = await self._retrieve_usecase.execute(
            file_id=file_id,
            bucket=bucket,
        )

        logger.info(f"[APP] File retrieved: id={meta.get_id()}, size={meta.get_size()}")
        return meta, stream

    async def delete(
        self,
        *,
        file_id: FileId,
        bucket: Buckets,
    ) -> None:
        if not self._delete_usecase:
            raise ApplicationRunTimeError("Delete usecase is not available")

        await self._delete_usecase.execute(
            file_id=file_id,
            bucket=bucket,
        )
        logger.info(f"[APP] File deleted: id={file_id}")

    async def update(
        self,
        *,
        bucket: Buckets,
        file_id: FileId,
        name: FileName,
        stream: Optional[AsyncIterator[bytes]] = None,
    ) -> FileMeta:
        if not self._update_usecase:
            raise ApplicationRunTimeError("Update usecase is not available")
        meta = await self._update_usecase.execute(
            file_id=file_id, name=name, stream=stream, bucket=bucket
        )
        logger.info(f"[APP] File updated: id={meta.get_id()}, size={meta.get_size()}")
        return meta
