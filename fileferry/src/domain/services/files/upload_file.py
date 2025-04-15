from typing import AsyncIterator
from domain.models.dataclasses import FileMeta
from domain.models.enums import FileStatus
from domain.protocols import UnitOfWork
from shared.io.peekable_stream import PeekableAsyncStream
from domain.services.files.policy import FilePolicy
from loguru import logger


class UploadFileService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def execute(self, file_id: str, file_name: str, data: AsyncIterator[bytes]):
        peekable = PeekableAsyncStream(data)
        header = await peekable.peek(2048)

        mime = FilePolicy.is_allowed(header)
        if not mime:
            raise Exception()

        size = await peekable.length()
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
                    stream=peekable.iter(),
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
