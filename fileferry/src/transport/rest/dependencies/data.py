from collections.abc import AsyncIterator

from fastapi import File, UploadFile


async def file_to_iterator(
    file: UploadFile = File(..., description="Binary file to be uploaded"),
) -> AsyncIterator[bytes]:
    """
    Возвращает асинхронный итератор из Strallete UploadFile.
    Не используется через FastAPI DI, потому что он вернет сразу
    весь объект (байты), а значит загрузит их в память.
    """
    while True:
        chunk = await file.read(4096)
        if not chunk:
            break
        yield chunk
