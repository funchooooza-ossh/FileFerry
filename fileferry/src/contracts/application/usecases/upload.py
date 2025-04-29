from collections.abc import AsyncIterator
from typing import Protocol

from domain.models import FileMeta, FileName
from shared.enums import Buckets


class UploadUseCaseContract(Protocol):
    async def execute(
        self, name: FileName, stream: AsyncIterator[bytes], bucket: Buckets
    ) -> FileMeta: ...
