from typing import Optional

from dependency_injector import containers, providers

from composition.factories.infrastructure import (
    cache_invalidator_factory,
    create_db_engine,
    create_transaction_context,
    create_transaction_manager,
    db_session_factory,
    db_sessionmaker,
    minio_client_factory,
    minio_storage_factory,
    redis_cache_storage_factory,
    redis_client_factory,
    resolve_data_access,
    sql_filemeta_data_access_factory,
    task_fire_n_forget_factory,
    task_manager_factory,
)
from contracts.infrastructure import FileMetaCacheStorageContract
from infrastructure.config.minio import MinioConfig
from infrastructure.config.postgres import PostgresSettings
from infrastructure.config.redis import RedisConfig
from infrastructure.coordination.minio_sqla import SqlAlchemyMinioCoordinator
from infrastructure.transactions.manager import TransactionManager


class InfrastructureContainer(containers.DeclarativeContainer):
    """Инфраструктурный DI-контейнер."""

    # --- Configs ---
    postgres_config = providers.Singleton(PostgresSettings)
    minio_config = providers.Singleton(MinioConfig)
    redis_config = providers.Singleton(RedisConfig)
    with_cache = providers.Configuration()

    # --- Session ---
    db_engine = providers.Singleton(
        create_db_engine,
        url=postgres_config.provided.url,
        echo=True,
    )

    db_sessionmaker = providers.Singleton(
        db_sessionmaker,
        engine=db_engine,
        autoflush=False,
        expire_on_commit=False,
    )

    db_session_factory = providers.Factory(
        db_session_factory, sessionmaker=db_sessionmaker
    )

    # --- Clients ---
    minio_client = providers.Singleton(minio_client_factory, config=minio_config)

    redis_client = providers.Singleton(
        redis_client_factory, config=redis_config, with_cache=with_cache
    )

    # --- Common Storage ---
    storage_access = providers.Factory(minio_storage_factory, client=minio_client)
    redis_storage: providers.Factory[Optional[FileMetaCacheStorageContract]] = (
        providers.Factory(
            redis_cache_storage_factory,
            with_cache=with_cache,
            client=redis_client,
            prefix="file:meta:",
        )
    )
    # --- Transaction Layer ---
    transaction = providers.ContextLocalSingleton(
        create_transaction_context,
        session_factory=db_session_factory,
    )
    transaction_manager: providers.Factory[TransactionManager] = providers.Factory(
        create_transaction_manager,
        context=transaction,
    )

    # --- Tasks ---
    task_manager = providers.Singleton(task_manager_factory, with_cache=with_cache)
    scheduler = providers.Singleton(task_fire_n_forget_factory, with_cache=with_cache)

    # --- Cache logic ---
    invalidator = providers.Factory(
        cache_invalidator_factory, storage=redis_storage, manager=task_manager
    )

    # --- Data Access ---
    sql_data_access = providers.Factory(
        sql_filemeta_data_access_factory, context=transaction
    )
    data_access = providers.Factory(
        resolve_data_access,
        with_cache=with_cache,
        scheduler=scheduler,
        redis_storage=redis_storage,
        invalidator=invalidator,
        sql_data_access=sql_data_access,
        ttl=300,
    )

    # --- Composition Root ---
    coordination: providers.Factory[SqlAlchemyMinioCoordinator] = providers.Factory(
        SqlAlchemyMinioCoordinator,
        transaction=transaction_manager,
        storage=storage_access,
        data_access=data_access,
    )
