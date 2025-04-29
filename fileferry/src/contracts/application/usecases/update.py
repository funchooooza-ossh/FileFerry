from collections.abc import AsyncIterator
from typing import Optional, Protocol

from domain.models import FileId, FileMeta, FileName
from shared.enums import Buckets


class UpdateUseCaseContract(Protocol):
    async def execute(
        self,
        file_id: FileId,
        name: FileName,
        stream: Optional[AsyncIterator[bytes]],
        bucket: Buckets,
    ) -> FileMeta: ...
