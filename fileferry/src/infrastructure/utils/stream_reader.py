from collections.abc import AsyncIterator


class AsyncStreamReader:
    def __init__(self, stream: AsyncIterator[bytes]) -> None:
        self._stream = stream.__aiter__()
        self._buffer = b""

    async def read(self, n: int = -1) -> bytes:
        while len(self._buffer) < n or n == -1:
            try:
                chunk = await self._stream.__anext__()
                self._buffer += chunk
            except StopAsyncIteration:
                break

        if n == -1:
            result, self._buffer = self._buffer, b""
        else:
            result, self._buffer = self._buffer[:n], self._buffer[n:]

        return result
