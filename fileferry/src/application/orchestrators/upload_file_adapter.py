from collections.abc import AsyncIterator, Callable

from contracts.application import FileAnalyzer, UploadFileService
from contracts.composition import UploadAPIAdapterContract
from domain.models.dataclasses import FileMeta
from shared.exceptions.application import DomainRejectedError
from shared.exceptions.domain import FilePolicyViolationEror


class UploadFileAPIAdapter(UploadAPIAdapterContract):
    def __init__(
        self,
        file_analyzer: FileAnalyzer,
        meta_factory: Callable[[str, int, str], FileMeta],
        upload_service: UploadFileService,
    ) -> None:
        self._analyzer = file_analyzer
        self._uploader = upload_service
        self._meta_factory = meta_factory

    async def create(
        self,
        name: str,
        stream: AsyncIterator[bytes],
    ) -> FileMeta:
        stream, mime, size = await self._analyzer.analyze(stream)
        meta = self._meta_factory(name, size, mime)

        try:
            return await self._uploader.execute(meta=meta, data=stream)
        except FilePolicyViolationEror as exc:
            raise DomainRejectedError("File rejected by policy", type=exc.type) from exc
