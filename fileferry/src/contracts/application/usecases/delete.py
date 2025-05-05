from typing import Protocol

from domain.models import FileId
from shared.enums import Buckets


class DeleteUseCaseContract(Protocol):
    async def execute(self, file_id: FileId, bucket: Buckets) -> None: ...
