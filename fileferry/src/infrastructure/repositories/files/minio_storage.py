from collections.abc import AsyncIterator

from aiohttp import ClientSession
from miniopy_async import Minio

from contracts.application import FileStorage
from infrastructure.utils.handlers.s3_handler import wrap_s3_failure
from infrastructure.utils.stream_reader import AsyncStreamReader


class MinioRepository(FileStorage):
    def __init__(self, client: Minio, bucket_name: str) -> None:
        self._client = client
        self._bucket = bucket_name

    @wrap_s3_failure
    async def store(
        self, file_id: str, stream: AsyncIterator[bytes], length: int, content_type: str
    ) -> None:
        stream = AsyncStreamReader(stream=stream)
        await self._client.put_object(
            bucket_name=self._bucket,
            object_name=file_id,
            data=stream,  # type: ignore AsyncStreamReader compatible with Minio SDK
            length=length,
            content_type=content_type,
        )

    @wrap_s3_failure
    async def retrieve(self, file_id: str) -> AsyncIterator[bytes]:
        session = ClientSession()
        response = await self._client.get_object(
            bucket_name=self._bucket,
            object_name=file_id,
            session=session,
        )

        async def stream() -> AsyncIterator[bytes]:
            try:
                async with response:
                    async for chunk in response.content.iter_chunked(4096):
                        yield chunk
            finally:
                await session.close()

        return stream()

    @wrap_s3_failure
    async def delete(self, file_id: str) -> None:
        await self._client.remove_object(bucket_name=self._bucket, object_name=file_id)
