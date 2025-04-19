from collections.abc import AsyncIterator
from typing import Protocol

from domain.models.dataclasses import FileMeta


class FileAnalyzer(Protocol):
    async def analyze(self, stream: AsyncIterator[bytes]) -> tuple[AsyncIterator[bytes], str, int]: ...


class FileService(Protocol):
    async def execute(self, meta: FileMeta, data: AsyncIterator[bytes]) -> FileMeta: ...
