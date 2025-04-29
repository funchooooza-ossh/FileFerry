from collections.abc import AsyncIterator
from typing import Protocol


class FileHelperContract(Protocol):
    @staticmethod
    async def analyze(
        stream: AsyncIterator[bytes],
    ) -> tuple[AsyncIterator[bytes], str, int]: ...
