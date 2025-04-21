from collections.abc import AsyncIterator
from typing import Protocol

from domain.models.dataclasses import FileMeta
from domain.models.value_objects import FileId


class FileAnalyzer(Protocol):
    async def analyze(self, stream: AsyncIterator[bytes]) -> tuple[AsyncIterator[bytes], str, int]: ...


class UploadFileService(Protocol):
    async def execute(self, meta: FileMeta, data: AsyncIterator[bytes]) -> FileMeta: ...


class RetrieveFileService(Protocol):
    async def execute(self, file_id: FileId) -> tuple[FileMeta, AsyncIterator[bytes]]: ...
