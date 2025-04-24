from collections.abc import AsyncIterator
from enum import StrEnum
from typing import Protocol, Union

from pydantic import BaseModel

from domain.models.dataclasses import FileMeta


class ScenarioName(StrEnum):
    MINIO_SQLA = "minio-sqla"
    SFTP_MONGO = "sftp-mongo"


class FileAction(StrEnum):
    UPLOAD = "upload"
    RETRIEVE = "retrieve"


class DependencyContext(BaseModel):
    scenario: ScenarioName
    bucket_name: str = "default-bucket"
    action: FileAction


class UploadAPIAdapterContract(Protocol):
    async def create(
        self,
        name: str,
        stream: AsyncIterator[bytes],
    ) -> FileMeta: ...


class RetrieveAPIAdapterContract(Protocol):
    async def get(self, file_id: str) -> tuple[FileMeta, AsyncIterator[bytes]]: ...


FileAPIAdapterContract = Union[UploadAPIAdapterContract, RetrieveAPIAdapterContract]
