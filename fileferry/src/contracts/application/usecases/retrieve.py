from collections.abc import AsyncIterator
from typing import Protocol

from shared.enums import Buckets


class RetrieveUseCaseContract(Protocol):
    async def execute(self, file_id: str, bucket: Buckets) -> AsyncIterator[bytes]: ...
