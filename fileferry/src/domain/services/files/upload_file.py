from typing import AsyncIterator
from domain.models.dataclasses import FileMeta
from domain.models.enums import FileStatus
from domain.protocols import UnitOfWork
from domain.utility.file_policy import FilePolicy
from domain.utility.file_helper import FileHelper
from loguru import logger


class UploadFileService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(
        self, file_id: str, file_name: str, data: AsyncIterator[bytes]
    ) -> FileMeta:
        stream = FileHelper.iterator_to_peekable_stream(data)
        header = FileHelper.get_stream_header(stream)
        mime = FileHelper.detect_mime(header)
        size = FileHelper.get_stream_size(stream)

        mime = FilePolicy.is_allowed(mime)
        if not mime:
            raise Exception()

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
                await self._uow.commit()
            except Exception as exc:
                logger.exception(exc)
                await self._uow.rollback()
                meta.status = FileStatus.FAILED
                return meta

        meta.status = FileStatus.STORED

        return meta
