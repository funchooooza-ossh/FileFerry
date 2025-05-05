from collections.abc import AsyncIterator

from fastapi import UploadFile


async def file_to_iterator(
    file: UploadFile, chunk_size: int = 4096
) -> AsyncIterator[bytes]:
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        yield chunk
