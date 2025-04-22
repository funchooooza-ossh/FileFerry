from collections.abc import AsyncIterator
from types import TracebackType
from typing import Protocol

from domain.models.dataclasses import FileMeta
from domain.models.value_objects import ContentType, FileId, FileSize


class FileAnalyzer(Protocol):
    async def analyze(self, stream: AsyncIterator[bytes]) -> tuple[AsyncIterator[bytes], str, int]: ...


class UploadFileService(Protocol):
    async def execute(self, meta: FileMeta, data: AsyncIterator[bytes]) -> FileMeta: ...


class RetrieveFileService(Protocol):
    async def execute(self, file_id: FileId) -> tuple[FileMeta, AsyncIterator[bytes]]: ...


class FileStorage(Protocol):
    async def store(self, file_id: str, stream: AsyncIterator[bytes], length: int, content_type: str) -> None: ...
    async def retrieve(self, file_id: str) -> AsyncIterator[bytes]: ...


class FileRepository(Protocol):
    async def add(self, file: FileMeta) -> None: ...
    async def get(self, file_id: str) -> FileMeta: ...


class UnitOfWork(Protocol):
    file_repo: FileRepository

    async def __aenter__(self) -> "UnitOfWork": ...
    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: TracebackType | None
    ) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...


class FilePolicy(Protocol):
    def is_allowewd(cls, mime: ContentType, size: FileSize) -> bool: ...
