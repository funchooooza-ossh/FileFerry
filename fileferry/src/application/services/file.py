from collections.abc import AsyncIterator, Callable

from application.protocols import FileAnalyzer, FileService
from composition.contracts import ApplicationFileService
from domain.models.dataclasses import FileMeta
from shared.exceptions.application import (
    DomainRejectedError,
    StatusFailedError,
)
from shared.exceptions.domain import FilePolicyViolationEror, FileUploadFailedError


class ApplicationFileServiceImpl(ApplicationFileService):
    def __init__(
        self,
        file_analyzer: FileAnalyzer,
        service: FileService,
        meta_factory: Callable[[str, int, str], FileMeta],
    ) -> None:
        self._analyzer = file_analyzer
        self._service = service
        self._meta_factory = meta_factory

    async def create(
        self,
        name: str,
        stream: AsyncIterator[bytes],
    ) -> FileMeta:
        stream, mime, size = await self._analyzer.analyze(stream)
        meta = self._meta_factory(name, size, mime)

        try:
            return await self._service.execute(meta=meta, data=stream)

        except FileUploadFailedError as exc:
            raise StatusFailedError("Upload failed", type=exc.type) from exc

        except FilePolicyViolationEror as exc:
            raise DomainRejectedError("File rejected by policy", type=exc.type) from exc
