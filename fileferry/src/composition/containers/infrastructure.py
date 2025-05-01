from collections.abc import Callable

from dependency_injector import containers, providers
from miniopy_async import Minio
from redis.asyncio import Redis
from redis.backoff import NoBackoff
from redis.retry import Retry
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from infrastructure.atomic.minio_sqla import SqlAlchemyMinioAtomicOperation
from infrastructure.config.minio import MinioConfig
from infrastructure.config.postgres import PostgresSettings
from infrastructure.config.redis import RedisConfig
from infrastructure.data_access.alchemy import SQLAlchemyDataAccess
from infrastructure.data_access.redis import CachedFileMetaAccess
from infrastructure.storage.minio import MiniOStorage
from infrastructure.storage.redis import RedisStorage
from infrastructure.tasks.consistence import CacheInvalidator
from infrastructure.tasks.manager import ImportantTaskManager
from infrastructure.tasks.scheduler import AsyncioTaskScheduler
from infrastructure.transactions.context import SqlAlchemyTransactionContext
from infrastructure.transactions.manager import TransactionManager


def create_transaction_context(
    session_factory: Callable[[], AsyncSession],
) -> SqlAlchemyTransactionContext:
    return SqlAlchemyTransactionContext(session=session_factory())


class InfrastructureContainer(containers.DeclarativeContainer):
    """Инфраструктурный DI-контейнер."""

    # --- Configs ---
    postgres_config = providers.Singleton(PostgresSettings)
    minio_config = providers.Singleton(MinioConfig)
    redis_config = providers.Singleton(RedisConfig)

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
        db_sessionmaker.provided.__call__
    )

    minio_client = providers.Singleton(
        Minio,
        endpoint=minio_config.provided.endpoint,
        access_key=minio_config.provided.access,
        secret_key=minio_config.provided.secret,
        secure=minio_config.provided.secure,
    )

    redis = providers.Singleton(
        Redis,
        host=redis_config.provided.host,
        port=redis_config.provided.port,
        socket_connect_timeout=redis_config.provided.socket_connect_timeout,
        socket_timeout=redis_config.provided.socket_timeout,
        retry=Retry(NoBackoff(), retries=0),
    )

    # --- Task Execution ---
    scheduler = providers.Singleton(AsyncioTaskScheduler)
    manager = providers.Singleton(ImportantTaskManager)

    # --- Storage ---
    storage_access = providers.Factory(MiniOStorage, client=minio_client)
    redis_storage = providers.Factory(RedisStorage, client=redis, prefix="file:meta")

    # --- Cache Logic ---
    cache_invalidator = providers.Singleton(
        CacheInvalidator, storage=redis_storage, manager=manager
    )

    sql_data_access = providers.Factory(SQLAlchemyDataAccess, session=None)
    cache_data_access = providers.Factory(
        CachedFileMetaAccess,
        invalidator=cache_invalidator,
        scheduler=scheduler,
        storage=redis_storage,
        ttl=300,
        delegate=None,
    )

    # --- Transaction Layer ---
    transaction: providers.Factory[SqlAlchemyTransactionContext] = providers.Factory(
        create_transaction_context,
        session_factory=db_session_factory,
    )
    transaction_manager: providers.Factory[TransactionManager] = providers.Factory(
        TransactionManager,
        context=transaction,
    )

    # --- Composition Root ---
    atomic_operation: providers.Factory[SqlAlchemyMinioAtomicOperation] = (
        providers.Factory(
            SqlAlchemyMinioAtomicOperation,
            transaction=transaction_manager,
            storage=storage_access,
            cache_aside=cache_data_access,
            sql_data_access=sql_data_access,
        )
    )
