from collections.abc import AsyncIterator

from miniopy_async import Minio

from infrastructure.utils.handlers.s3_handler import wrap_s3_failure
from infrastructure.utils.stream_reader import AsyncStreamReader


class MinioRepository:
    def __init__(self, client: Minio, bucket_name: str) -> None:
        self._client = client
        self._bucket = bucket_name

    @wrap_s3_failure
    async def store(self, file_id: str, stream: AsyncIterator[bytes], length: int, content_type: str) -> None:
        stream = AsyncStreamReader(stream)
        await self._client.put_object(
            bucket_name=self._bucket,
            object_name=file_id,
            data=stream,
            length=length,
            content_type=content_type,
        )

    @wrap_s3_failure
    async def retrieve(self, file_id: str) -> AsyncIterator[bytes]:
        response = await self._client.get_object(
            bucket_name=self._bucket, object_name=file_id, session=self._client._client_session()
        )

        async def stream() -> AsyncIterator[bytes]:
            async with response:
                async for chunk in response.content.iter_chunked(4096):
                    yield chunk

        return stream()
