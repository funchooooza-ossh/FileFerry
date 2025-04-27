from typing import Protocol

from shared.enums import Buckets


class DeleteUseCaseContract(Protocol):
    async def execute(self, file_id: str, bucket: Buckets) -> None: ...
