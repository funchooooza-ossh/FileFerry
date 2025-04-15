from fastapi import UploadFile
from typing import AsyncIterator


async def file_to_iterator(
    file: UploadFile, chunk_size: int = 4096
) -> AsyncIterator[bytes]:
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        yield chunk
