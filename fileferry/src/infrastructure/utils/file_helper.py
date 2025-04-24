from collections.abc import AsyncIterator

from magic import Magic

from contracts.application import FileAnalyzer
from shared.io.peekable_stream import PeekableAsyncStream


class FileHelper(FileAnalyzer):
    @staticmethod
    async def analyze(
        stream: AsyncIterator[bytes],
    ) -> tuple[AsyncIterator[bytes], str, int]:
        peek = FileHelper.iterator_to_peekable_stream(stream)

        header = await FileHelper.get_stream_header(peek)

        mime = FileHelper.detect_mime(header)
        size = await FileHelper.get_stream_size(peek)

        return peek.iter(), mime, size

    @staticmethod
    def iterator_to_peekable_stream(
        iterator: AsyncIterator[bytes],
    ) -> PeekableAsyncStream:
        return PeekableAsyncStream(source=iterator)

    @staticmethod
    async def get_stream_header(stream: PeekableAsyncStream, chunk: int = 2048) -> bytes:
        return await stream.peek(2048)

    @staticmethod
    def detect_mime(header: bytes) -> str:
        return Magic(mime=True).from_buffer(buf=header)

    @staticmethod
    async def get_stream_size(stream: PeekableAsyncStream) -> int:
        return await stream.length()
