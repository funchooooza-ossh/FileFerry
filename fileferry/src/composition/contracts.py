from collections.abc import AsyncIterator
from typing import Literal, Protocol

from pydantic import BaseModel

from domain.models.dataclasses import FileMeta


class DependencyContext(BaseModel):
    scenario: Literal["minio-sqla", "sftp-mongo"]
    bucket_name: str = "default-bucket"
    action: Literal["get", "upload"]


class ApplicationFileService(Protocol):
    async def create(
        self,
        name: str,
        stream: AsyncIterator[bytes],
    ) -> FileMeta: ...
