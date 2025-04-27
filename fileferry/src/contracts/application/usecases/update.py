from collections.abc import AsyncIterator
from typing import Optional, Protocol

from domain.models import FileMeta


class UpdateUseCaseContract(Protocol):
    async def execute(
        self, file_id: str, name: Optional[str], stream: Optional[AsyncIterator[bytes]]
    ) -> FileMeta: ...
