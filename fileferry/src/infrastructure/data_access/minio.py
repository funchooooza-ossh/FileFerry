from collections.abc import AsyncIterator

from loguru import logger
from miniopy_async import Minio

from contracts.infrastructure import StorageAccessContract
from domain.models import FileMeta
from infrastructure.http.create_clientsession import create_client_session
from infrastructure.utils.stream_reader import AsyncStreamReader
from shared.enums import Buckets
from shared.exceptions.handlers.s3_handler import wrap_s3_failure


class MiniOStorage(StorageAccessContract):
    def __init__(self, client: Minio) -> None:
        self._client = client

    @wrap_s3_failure
    async def upload(
        self, *, file_meta: FileMeta, stream: AsyncIterator[bytes], bucket: Buckets
    ) -> None:
        stream_reader = AsyncStreamReader(stream)
        await self._client.put_object(
            bucket_name=bucket.value,
            object_name=file_meta.id.value,
            length=file_meta.size.value,
            content_type=file_meta.content_type.value,
            data=stream_reader,  # type: ignore
        )
        return

    @wrap_s3_failure
    async def retrieve(self, *, file_id: str, bucket: Buckets) -> AsyncIterator[bytes]:
        async def stream() -> AsyncIterator[bytes]:
            async with create_client_session() as session:
                response = await self._client.get_object(
                    bucket_name=bucket, object_name=file_id, session=session
                )
                async with response:
                    async for chunk in response.content.iter_chunked(4096):
                        yield chunk

        return stream()

    @wrap_s3_failure
    async def delete(self, *, file_id: str, bucket: Buckets) -> None:
        await self._client.remove_object(bucket.value, file_id)

    async def healtcheck(self) -> bool:
        try:
            response = await self._client.list_buckets()
            return bool(response)
        except Exception as exc:
            logger.critical(f"[MiniO] Storage healtcheck failed: {exc}")
            return False
