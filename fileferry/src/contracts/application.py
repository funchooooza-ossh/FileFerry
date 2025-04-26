from collections.abc import AsyncIterator
from types import TracebackType
from typing import Protocol

from domain.models.dataclasses import FileMeta
from domain.models.value_objects import ContentType, FileId, FileSize
from infrastructure.config.minio import ExistingBuckets
from shared.types.healthcheck import (
    RepoHealthStatus,
    ServiceHealthStatus,
    StorageHealthStatus,
)


class FileAnalyzer(Protocol):
    @staticmethod
    async def analyze(
        stream: AsyncIterator[bytes],
    ) -> tuple[AsyncIterator[bytes], str, int]: ...


class UploadFileService(Protocol):
    async def execute(
        self, meta: FileMeta, data: AsyncIterator[bytes], bucket: ExistingBuckets
    ) -> FileMeta: ...


class RetrieveFileService(Protocol):
    async def execute(
        self, file_id: FileId, bucket: ExistingBuckets
    ) -> tuple[FileMeta, AsyncIterator[bytes]]: ...


class HealthCheckService(Protocol):
    async def execute(self) -> ServiceHealthStatus: ...


class DeleteFileService(Protocol):
    async def execute(self, file_id: FileId, bucket: ExistingBuckets) -> None: ...


class FileStorage(Protocol):
    async def store(
        self,
        file_id: str,
        stream: AsyncIterator[bytes],
        length: int,
        content_type: str,
        bucket: ExistingBuckets,
    ) -> None: ...
    async def retrieve(
        self, file_id: str, bucket: ExistingBuckets
    ) -> AsyncIterator[bytes]: ...
    async def delete(self, file_id: str, bucket: ExistingBuckets) -> None: ...
    async def healthcheck(self) -> StorageHealthStatus: ...


class FileRepository(Protocol):
    async def add(self, file_meta: FileMeta) -> None: ...
    async def get(self, file_id: str) -> FileMeta: ...
    async def delete(self, file_id: str) -> None: ...
    async def healthcheck(self) -> RepoHealthStatus: ...


class UnitOfWork(Protocol):
    @property
    def file_repo(
        self,
    ) -> FileRepository: ...

    """
    говорим pylance, что наш аттрибут file_repo - property,
    и он никогда не None, на деле же при инициализации мы можем
    lazy-инитить его
    но в реализации можно делать ClassVar или через конструктор.
    почему так? мы не передаем готовый репозиторий в UoW никогда,
    напротив он сам управляет сессией и создает репозиторий с готовой сессией.

    """

    async def __aenter__(self) -> "UnitOfWork": ...
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...


class FilePolicy(Protocol):
    FORBIDDEN_TYPES: set[str]

    @classmethod
    def is_allowed(cls, mime: ContentType, size: FileSize) -> bool: ...
