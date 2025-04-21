from collections.abc import AsyncIterator
from enum import StrEnum
from typing import Literal, Protocol

from pydantic import BaseModel

from domain.models.dataclasses import FileMeta


class ScenarioName(StrEnum):
    MINIO_SQLA = "minio-sqla"
    SFTP_MONGO = "sftp-mongo"

class DependencyContext(BaseModel):
    scenario: ScenarioName
    bucket_name: str = "default-bucket"
    action: Literal["get", "upload"]


class ApplicationFileService(Protocol):
    async def create(
        self,
        name: str,
        stream: AsyncIterator[bytes],
    ) -> FileMeta: ...

    async def get(self, file_id: str) -> tuple[FileMeta, AsyncIterator[bytes]]: ...
