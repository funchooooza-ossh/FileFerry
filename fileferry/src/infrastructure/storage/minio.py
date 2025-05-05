import time
from collections.abc import AsyncIterator

from miniopy_async import Minio
from miniopy_async.error import S3Error

from contracts.infrastructure import StorageAccessContract
from domain.models import FileMeta
from infrastructure.http.create_clientsession import create_client_session
from infrastructure.utils.stream_reader import AsyncStreamReader
from shared.enums import Buckets
from shared.exceptions.handlers.s3_handler import wrap_s3_failure
from shared.types.component_health import ComponentStatus


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
            object_name=file_meta.get_id(),
            length=file_meta.get_size(),
            content_type=file_meta.get_content_type(),
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

    async def healthcheck(self) -> ComponentStatus:
        start = time.perf_counter()
        try:
            buckets = [str(bucket) for bucket in await self._client.list_buckets()]
            latency = (time.perf_counter() - start) * 1000  # в миллисекундах

            status = "ok" if latency <= 150.0 else "degraded"

            return ComponentStatus(
                status=status,
                latency_ms=latency,
                details={"buckets_count": str(len(buckets)), "buckets": buckets},
            )

        except S3Error as exc:
            return ComponentStatus(status="down", error=f"{exc.code}:{exc.message}")
        except Exception as exc:
            return ComponentStatus(status="down", error=str(exc))
