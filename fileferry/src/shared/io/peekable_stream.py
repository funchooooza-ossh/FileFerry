from collections import deque
from typing import AsyncIterator, Deque
import asyncio


class PeekableAsyncStream:
    def __init__(self, source: AsyncIterator[bytes]):
        self._source = source
        self._buffer: Deque[bytes] = deque()
        self._cached: list[bytes] = []
        self._fully_buffered = False
        self._lock = asyncio.Lock()

    async def peek(self, size: int) -> bytes:
        async with self._lock:
            collected = b"".join(self._buffer)
            while len(collected) < size and not self._fully_buffered:
                try:
                    chunk = await self._source.__anext__()
                    self._buffer.append(chunk)
                    self._cached.append(chunk)
                    collected += chunk
                except StopAsyncIteration:
                    self._fully_buffered = True
                    break
            return collected[:size]

    async def length(self) -> int:
        async with self._lock:
            if self._fully_buffered:
                return sum(len(chunk) for chunk in self._cached)

            async for chunk in self._source:
                self._buffer.append(chunk)
                self._cached.append(chunk)
            self._fully_buffered = True
            return sum(len(chunk) for chunk in self._cached)

    def iter(self) -> AsyncIterator[bytes]:
        return self._stream()

    async def _stream(self):
        async with self._lock:
            while self._buffer:
                yield self._buffer.popleft()
            if not self._fully_buffered:
                async for chunk in self._source:
                    yield chunk
