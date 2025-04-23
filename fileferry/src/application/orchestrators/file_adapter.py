from collections.abc import AsyncIterator, Callable
from typing import Optional

from contracts.application import FileAnalyzer, RetrieveFileService, UploadFileService
from contracts.composition import FileAPIAdapterContract
from domain.models.dataclasses import FileMeta
from domain.models.value_objects import FileId
from shared.exceptions.application import DomainRejectedError, InvalidValueError
from shared.exceptions.domain import FilePolicyViolationEror


class FileAPIAdapter(FileAPIAdapterContract):
    def __init__(
        self,
        file_analyzer: FileAnalyzer,
        meta_factory: Callable[[str, int, str], FileMeta],
        upload_service: Optional[UploadFileService] = None,
        retrieve_service: Optional[RetrieveFileService] = None,
    ) -> None:
        if (upload_service is None) == (retrieve_service is None):
            raise ValueError("Provide exactly one of upload_service or retrieve_service")

        self._analyzer = file_analyzer
        self._uploader = upload_service
        self._retriever = retrieve_service
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

    async def get(self, file_id: str) -> tuple[FileMeta, AsyncIterator[bytes]]:
        try:
            file_id_vo = FileId(value=file_id)
        except ValueError as exc:
            raise InvalidValueError("Невалидный id файла") from exc

        return await self._retriever.execute(file_id=file_id_vo)
