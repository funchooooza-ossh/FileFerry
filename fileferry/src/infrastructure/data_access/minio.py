import contextlib
from collections.abc import AsyncIterator

from miniopy_async import Minio, S3Error
from miniopy_async.commonconfig import CopySource

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
    async def stage_upload(
        self, *, file_meta: FileMeta, stream: AsyncIterator[bytes], bucket: Buckets
    ) -> str:
        tmp_file_id = f"{file_meta.id.value}.tmp"
        stream_reader = AsyncStreamReader(stream)

        await self._client.put_object(
            bucket_name=bucket,
            object_name=tmp_file_id,
            data=stream_reader,  # type: ignore
            length=file_meta.size.value,
            content_type=file_meta.content_type.value,
        )

        return tmp_file_id

    @wrap_s3_failure
    async def retrieve(self, *, file_id: str, bucket: Buckets) -> AsyncIterator[bytes]:
        async with create_client_session() as session:
            response = await self._client.get_object(
                bucket_name=bucket, object_name=file_id, session=session
            )

            async def stream() -> AsyncIterator[bytes]:
                async with response:
                    async for chunk in response.content.iter_chunked(4096):
                        yield chunk

            return stream()

    @wrap_s3_failure
    async def commit(
        self, *, staged_file_id: str, final_file_id: str, bucket: str
    ) -> None:
        await self._client.copy_object(
            bucket_name=bucket,
            object_name=final_file_id,
            source=CopySource(object_name=staged_file_id, bucket_name=bucket),
        )
        await self._client.remove_object(bucket, staged_file_id)

    async def rollback(self, *, staged_file_id: str, bucket: Buckets) -> None:
        """Удаляет временный файл при ошибке."""
        with contextlib.suppress(S3Error):
            await self._client.remove_object(bucket, staged_file_id)

    @wrap_s3_failure
    async def delete(self, *, file_id: str, bucket: Buckets) -> None:
        await self._client.remove_object(bucket.value, file_id)
