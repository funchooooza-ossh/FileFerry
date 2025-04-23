from collections.abc import AsyncIterator

from miniopy_async import Minio
from miniopy_async.error import S3Error

from infrastructure.enums.s3error import CODE_TO_ERROR_MAPPING, S3ErrorCode
from infrastructure.utils.stream_reader import AsyncStreamReader
from shared.exceptions.infrastructure import StorageError


class MinioRepository:
    def __init__(self, client: Minio, bucket_name: str) -> None:
        self._client = client
        self._bucket = bucket_name

    async def store(self, file_id: str, stream: AsyncIterator[bytes], length: int, content_type: str) -> None:
        try:
            stream = AsyncStreamReader(stream)
            await self._client.put_object(
                bucket_name=self._bucket,
                object_name=file_id,
                data=stream,
                length=length,
                content_type=content_type,
            )
        except S3Error as exc:
            err_cls = CODE_TO_ERROR_MAPPING.get(S3ErrorCode(exc.code), StorageError)
            raise err_cls(f"S3 error while upload: {exc.message}") from exc
        except Exception as exc:
            raise StorageError(f"Unexpected error: {exc}") from exc

    async def retrieve(self, file_id: str) -> AsyncIterator[bytes]:
        try:
            response = await self._client.get_object(
                bucket_name=self._bucket, object_name=file_id, session=self._client._client_session()
            )

            async def stream() -> AsyncIterator[bytes]:
                async with response:
                    async for chunk in response.content.iter_chunked(4096):
                        yield chunk

            return stream()
        except S3Error as exc:
            err_cls = CODE_TO_ERROR_MAPPING.get(S3ErrorCode(exc.code), StorageError)
            raise err_cls(f"S3 error while retrieve: {exc.message}") from exc
        except Exception as exc:
            raise StorageError(f"Unexpected error: {exc}") from exc
