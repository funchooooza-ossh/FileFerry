from magic import Magic
from typing import AsyncIterator
from shared.io.peekable_stream import PeekableAsyncStream


class FileHelper:
    @staticmethod
    def iterator_to_peekable_stream(
        iterator: AsyncIterator[bytes],
    ) -> PeekableAsyncStream:
        return PeekableAsyncStream(source=iterator)

    @staticmethod
    async def get_stream_header(
        stream: PeekableAsyncStream, chunk: int = 2048
    ) -> bytes:
        return await stream.peek(2048)

    @staticmethod
    def detect_mime(header: bytes) -> str:
        return Magic(mime=True).from_buffer(buf=header)

    @staticmethod
    async def get_stream_size(stream: PeekableAsyncStream) -> int:
        return await stream.length()
