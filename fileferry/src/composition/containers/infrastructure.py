from collections.abc import Callable

from dependency_injector import containers, providers
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from infrastructure.atomic.minio_sqla import SqlAlchemyMinioAtomicOperation
from infrastructure.config.minio import MinioConfig
from infrastructure.config.postgres import PostgresSettings
from infrastructure.data_access.alchemy import SQLAlchemyDataAccess
from infrastructure.storage.minio import MiniOStorage
from infrastructure.transactions.context import SqlAlchemyTransactionContext
from infrastructure.transactions.manager import TransactionManager


def create_transaction_context(
    session_factory: Callable[[], AsyncSession],
) -> SqlAlchemyTransactionContext:
    session = session_factory()
    return SqlAlchemyTransactionContext(session=session)


class InfrastructureContainer(containers.DeclarativeContainer):
    """Контейнер инфраструктуры: БД, MinIO, доступ к данным."""

    postgres_config = providers.Singleton(PostgresSettings)
    minio_config = providers.Singleton(MinioConfig)

    # --- Clients ---
    db_engine = providers.Singleton(
        create_async_engine,
        url=postgres_config.provided.url,
        echo=False,
        future=True,
    )

    db_sessionmaker = providers.Singleton(
        async_sessionmaker,
        bind=db_engine,
        autoflush=False,
        expire_on_commit=False,
        future=True,
    )

    db_session_factory: providers.Factory[AsyncSession] = providers.Factory(
        db_sessionmaker.provided.__call__,
    )

    minio_client = providers.Singleton(
        Minio,
        endpoint=minio_config.provided.endpoint,
        access_key=minio_config.provided.access,
        secret_key=minio_config.provided.secret,
        secure=minio_config.provided.secure,
    )

    # --- Gateways ---
    storage_access = providers.Factory(
        MiniOStorage,
        client=minio_client,
    )

    # DataAccess пока без сессии, будет передаваться в UoW
    data_access = providers.Factory(SQLAlchemyDataAccess, session=None)

    # --- Unit of Work / Transaction ---
    transaction = providers.Factory(
        create_transaction_context,
        session_factory=db_session_factory,
    )
    transaction_manager = providers.Factory(TransactionManager, context=transaction)

    atomic_operation: providers.Factory[SqlAlchemyMinioAtomicOperation] = (
        providers.Factory(
            SqlAlchemyMinioAtomicOperation,
            transaction=transaction_manager,
            storage=storage_access,
            data_access=data_access,
        )
    )
