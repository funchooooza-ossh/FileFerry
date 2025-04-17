from miniopy_async import Minio
from typing import AsyncIterator
from shared.exceptions.infrastructure import StorageError, StorageNotFoundError
from infrastructure.utils.stream_reader import AsyncStreamReader


class MinioRepository:
    def __init__(self, client: Minio, bucket_name: str):
        self._client = client
        self._bucket = bucket_name

    async def store(
        self, file_id: str, stream: AsyncIterator[bytes], length: int, content_type: str
    ) -> None:
        try:
            stream = AsyncStreamReader(stream)
            await self._client.put_object(
                bucket_name=self._bucket,
                object_name=file_id,
                data=stream,
                length=length,
                content_type=content_type,
            )
        except Exception as exc:
            raise StorageError(f"{type(exc).__name__}: {exc}") from exc

    async def retrieve(self, file_id: str) -> AsyncIterator[bytes]:
        try:
            response = await self._client.get_object(self._bucket, file_id)
            async for chunk in response.stream(4096):
                yield chunk
        except Exception as exc:
            raise StorageNotFoundError(f"Object {file_id} not found") from exc
