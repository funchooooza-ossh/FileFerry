from collections.abc import Callable

from dependency_injector import containers, providers
from miniopy_async import Minio
from redis.asyncio import Redis
from redis.backoff import NoBackoff
from redis.retry import Retry
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from infrastructure.config.minio import MinioConfig
from infrastructure.config.postgres import PostgresSettings
from infrastructure.config.redis import RedisConfig
from infrastructure.coordination.minio_sqla import SqlAlchemyMinioCoordinator
from infrastructure.data_access.alchemy import SQLAlchemyFileMetaDataAccess
from infrastructure.data_access.redis import CachedFileMetaDataAccess
from infrastructure.storage.minio import MiniOStorage
from infrastructure.storage.redis import RedisFileMetaCacheStorage
from infrastructure.tasks.consistence import CacheInvalidator
from infrastructure.tasks.manager import ImportantTaskManager, NoOpImportantTaskManager
from infrastructure.tasks.scheduler import AsyncioFireAndForget
from infrastructure.transactions.context import SqlAlchemyTransactionContext
from infrastructure.transactions.manager import TransactionManager


def create_transaction_context(
    session_factory: Callable[[], AsyncSession],
) -> SqlAlchemyTransactionContext:
    return SqlAlchemyTransactionContext(session=session_factory())


@providers.Factory
def data_access_factory(
    with_cache: bool,
    redis_client: Redis | None,
    sql_data_access: SQLAlchemyFileMetaDataAccess,
    task_manager: ImportantTaskManager,
    scheduler: AsyncioFireAndForget | None,
) -> SQLAlchemyFileMetaDataAccess | CachedFileMetaDataAccess:
    if not scheduler or not redis_client or not with_cache:
        return sql_data_access
    redis_storage = RedisFileMetaCacheStorage(
        client=redis_client,
        prefix="file:meta",
    )
    invalidator = CacheInvalidator(
        cache_storage=redis_storage,
        task_manager=task_manager,
    )
    return CachedFileMetaDataAccess(
        invalidator=invalidator,
        scheduler=scheduler,
        storage=redis_storage,
        ttl=300,
        delegate=sql_data_access,
    )


@providers.Singleton
def task_manager_factory(
    with_cache: bool,
) -> ImportantTaskManager | NoOpImportantTaskManager:
    if not with_cache:
        return NoOpImportantTaskManager()
    return ImportantTaskManager()


@providers.Singleton
def task_fire_n_forget_factory(with_cache: bool) -> AsyncioFireAndForget | None:
    if not with_cache:
        return None
    return AsyncioFireAndForget()


@providers.Singleton
def redis_client_factory(config: RedisConfig, with_cache: bool) -> Redis | None:
    if not with_cache:
        return None
    return Redis(
        host=config.host,
        port=config.port,
        socket_connect_timeout=config.socket_connect_timeout,
        socket_timeout=config.socket_timeout,
        retry=Retry(NoBackoff(), retries=0),  # type: ignore
    )


class InfrastructureContainer(containers.DeclarativeContainer):
    """Инфраструктурный DI-контейнер."""

    # --- Configs ---
    postgres_config = providers.Singleton(PostgresSettings)
    minio_config = providers.Singleton(MinioConfig)
    redis_config = providers.Singleton(RedisConfig)
    with_cache = providers.Configuration()

    # --- Clients ---
    db_engine = providers.Singleton(
        create_async_engine,
        url=postgres_config.provided.url,
        echo=True,
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

    redis_client = providers.Singleton(
        redis_client_factory, config=redis_config, with_cache=with_cache
    )

    # --- Transaction Layer ---
    transaction: providers.Resource[SqlAlchemyTransactionContext] = providers.Resource(
        create_transaction_context,
        session_factory=db_session_factory,
    )
    transaction_manager: providers.Factory[TransactionManager] = providers.Factory(
        TransactionManager,
        context=transaction,
    )
    sql_data_access = providers.Factory(
        SQLAlchemyFileMetaDataAccess, context=transaction
    )

    # --- Tasks ---
    task_manager = providers.Singleton(task_manager_factory, with_cache=with_cache)
    scheduler = providers.Singleton(task_fire_n_forget_factory, with_cache=with_cache)
    # --- Common Storage ---
    storage_access = providers.Factory(MiniOStorage, client=minio_client)
    data_access = providers.Factory(
        data_access_factory,
        with_cache=with_cache,
        redis_client=redis_client,
        sql_data_access=sql_data_access,
        task_manager=task_manager,
        scheduler=scheduler,
    )

    # --- Composition Root ---
    coordination: providers.Factory[SqlAlchemyMinioCoordinator] = providers.Factory(
        SqlAlchemyMinioCoordinator,
        transaction=transaction_manager,
        storage=storage_access,
        data_access=data_access,
    )
