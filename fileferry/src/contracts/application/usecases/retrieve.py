from collections.abc import AsyncIterator
from typing import Protocol

from domain.models import FileId, FileMeta
from shared.enums import Buckets


class RetrieveUseCaseContract(Protocol):
    async def execute(
        self, file_id: FileId, bucket: Buckets
    ) -> tuple[FileMeta, AsyncIterator[bytes]]: ...
