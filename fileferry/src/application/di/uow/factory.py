from typing import Literal, Callable, AsyncGenerator, Final
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.uow.minio_sqla import SQLAlchemyMinioUnitOfWork
from infrastructure.db.session import get_async_session
from application.di.minio.factory import create_minio_client
from application.di.minio.registry import KnownMinioClients

KnownUoW = Literal["minio-sqla", "sftp-mongo"]


class UnitOfWorkFactory:
    LITERAL_CONFIGURATION_MAPPING: Final[dict[KnownUoW, Callable]] = {
        "minio-sqla": lambda **kwargs: UnitOfWorkFactory.create_minio_sqlalchemy(
            **kwargs
        ),
    }

    @classmethod
    def create(cls, config: KnownUoW, **kwargs) -> Callable:
        factory_method = cls.LITERAL_CONFIGURATION_MAPPING.get(config)
        if not factory_method:
            raise ValueError(f"Unknown UnitOfWork configuration: {config}")
        return factory_method(**kwargs)

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
