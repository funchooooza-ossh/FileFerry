from collections.abc import AsyncIterator
from typing import Optional

from contracts.application import (
    ApplicationAdapterContract,
    DeleteUseCaseContract,
    HealthCheckUseCaseContract,
    RetrieveUseCaseContract,
    UpdateUseCaseContract,
    UploadUseCaseContract,
)
from domain.models import FileMeta, HealthReport
from shared.enums import Buckets
from shared.exceptions.exc_classes.application import ApplicationRunTimeError


class FileApplicationAdapter(ApplicationAdapterContract):
    """Адаптер для операций над файлами."""

    def __init__(
        self,
        upload_usecase: Optional[UploadUseCaseContract] = None,
        retrieve_usecase: Optional[RetrieveUseCaseContract] = None,
        delete_usecase: Optional[DeleteUseCaseContract] = None,
        update_usecase: Optional[UpdateUseCaseContract] = None,
        health_usecase: Optional[HealthCheckUseCaseContract] = None,
    ) -> None:
        self._upload_usecase = upload_usecase
        self._retrieve_usecase = retrieve_usecase
        self._delete_usecase = delete_usecase
        self._update_usecase = update_usecase
        self._health_usecase = health_usecase

    async def upload(
        self,
        *,
        name: str,
        stream: AsyncIterator[bytes],
        bucket: Buckets,
    ) -> FileMeta:
        if not self._upload_usecase:
            raise ApplicationRunTimeError("Upload usecase is not available")

        return await self._upload_usecase.execute(
            name=name,
            stream=stream,
            bucket=bucket,
        )

    async def retrieve(
        self,
        *,
        file_id: str,
        bucket: Buckets,
    ) -> tuple[FileMeta, AsyncIterator[bytes]]:
        if not self._retrieve_usecase:
            raise ApplicationRunTimeError("Retrieve usecase is not available")

        return await self._retrieve_usecase.execute(
            file_id=file_id,
            bucket=bucket,
        )

    async def delete(
        self,
        *,
        file_id: str,
        bucket: Buckets,
    ) -> None:
        if not self._delete_usecase:
            raise ApplicationRunTimeError("Delete usecase is not available")

        await self._delete_usecase.execute(
            file_id=file_id,
            bucket=bucket,
        )

    async def update(
        self,
        *,
        bucket: Buckets,
        file_id: str,
        name: str,
        stream: Optional[AsyncIterator[bytes]] = None,
    ) -> FileMeta:
        if not self._update_usecase:
            raise ApplicationRunTimeError("Update usecase is not available")
        return await self._update_usecase.execute(
            file_id=file_id, name=name, stream=stream, bucket=bucket
        )

    async def healthcheck(self) -> HealthReport:
        if not self._health_usecase:
            raise ApplicationRunTimeError("Health usecase is not available")
        return await self._health_usecase.execute()
