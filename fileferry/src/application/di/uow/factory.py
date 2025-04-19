from collections.abc import AsyncGenerator, Callable
from typing import Any, Literal

from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession

from application.di.minio.factory import create_minio_client
from application.di.minio.registry import KnownMinioClients
from infrastructure.db.session import get_async_session
from infrastructure.uow.minio_sqla import SQLAlchemyMinioUnitOfWork

KnownUoW = Literal["minio-sqla", "sftp-mongo"]


class UnitOfWorkFactory:
    @classmethod
    def create(cls, config: KnownUoW, **kwargs: Any) -> Callable:
        match config:
            case "minio-sqla":
                return cls.create_minio_sqlalchemy(**kwargs)
            case "sftp-mongo":
                return
            case _:
                raise ValueError("Unknown UoW")

    @staticmethod
    def create_minio_sqlalchemy(
        session_factory: AsyncGenerator[AsyncSession, None] = get_async_session,
        bucket_name: str = "default-bucket",
        minio_factory: Callable[[KnownMinioClients], Minio] = create_minio_client,
        minio_type: KnownMinioClients = "default",
    ) -> SQLAlchemyMinioUnitOfWork:
        client = minio_factory(minio_type)
        return SQLAlchemyMinioUnitOfWork(
            session_factory=session_factory,
            bucket_name=bucket_name,
            client=client,
        )
