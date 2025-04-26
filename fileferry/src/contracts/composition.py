from collections.abc import AsyncIterator
from enum import StrEnum
from typing import Protocol, Union

from pydantic import BaseModel

from domain.models.dataclasses import FileMeta
from infrastructure.config.minio import ExistingBuckets
from shared.types.healthcheck import ServiceHealthStatus


class ScenarioName(StrEnum):
    MINIO_SQLA = "minio-sqla"
    # SFTP_MONGO = "sftp-mongo"


class FileAction(StrEnum):
    UPLOAD = "upload"
    RETRIEVE = "retrieve"
    DELETE = "delete"
    HEALTH = "health"


class DependencyContext(BaseModel):
    scenario: ScenarioName
    bucket_name: ExistingBuckets
    action: FileAction


class UploadAPIAdapterContract(Protocol):
    async def create(
        self, name: str, stream: AsyncIterator[bytes], bucket: ExistingBuckets
    ) -> FileMeta: ...


class RetrieveAPIAdapterContract(Protocol):
    async def get(
        self, file_id: str, bucket: ExistingBuckets
    ) -> tuple[FileMeta, AsyncIterator[bytes]]: ...


class DeleteAPIAdapterContract(Protocol):
    async def delete(self, file_id: str, bucket: ExistingBuckets) -> None: ...


class HealthCheckAPIAdapterContract(Protocol):
    async def healthcheck(self) -> ServiceHealthStatus: ...


FileAPIAdapterContract = Union[
    UploadAPIAdapterContract,
    RetrieveAPIAdapterContract,
    DeleteAPIAdapterContract,
    HealthCheckAPIAdapterContract,
]
