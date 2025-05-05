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
from infrastructure.config.minio import MinioConfig
from infrastructure.config.postgres import PostgresSettings
from infrastructure.config.redis import RedisConfig
from infrastructure.coordination.minio_sqla import SqlAlchemyMinioCoordinator


class InfrastructureContainer(containers.DeclarativeContainer):
    """Инфраструктурный DI-контейнер."""

    # --- Configs ---
    config_postgres = providers.Singleton(PostgresSettings)
    config_minio = providers.Singleton(MinioConfig)
    config_redis = providers.Singleton(RedisConfig)
    enable_cache = providers.Configuration()

    # --- Clients ---
    engine_postgres = providers.Singleton(
        create_db_engine,
        url=config_postgres.provided.url,
        echo=True,
    )

    sessionmaker_postgres = providers.Singleton(
        db_sessionmaker,
        engine=engine_postgres,
        autoflush=False,
        expire_on_commit=False,
    )

    session_factory = providers.Factory(
        db_session_factory,
        sessionmaker=sessionmaker_postgres,
    )

    client_minio = providers.Singleton(minio_client_factory, config=config_minio)
    client_redis = providers.Singleton(
        redis_client_factory, config=config_redis, with_cache=enable_cache
    )

    # --- Transaction Layer ---
    tx_context = providers.ContextLocalSingleton(
        create_transaction_context,
        session_factory=session_factory,
    )
    tx_manager = providers.Factory(
        create_transaction_manager,
        context=tx_context,
    )
    dao_sqlalchemy = providers.Factory(
        sql_filemeta_data_access_factory,
        context=tx_context,
    )

    # --- Tasks ---
    task_exec = providers.Singleton(task_manager_factory, with_cache=enable_cache)
    task_scheduler = providers.Singleton(
        task_fire_n_forget_factory, with_cache=enable_cache
    )

    # --- Storages ---
    storage_minio = providers.Factory(minio_storage_factory, client=client_minio)
    storage_redis = providers.Factory(
        redis_cache_storage_factory,
        with_cache=enable_cache,
        client=client_redis,
        prefix="file:meta:",
    )

    cache_invalidator = providers.Factory(
        cache_invalidator_factory,
        storage=storage_redis,
        manager=task_exec,
    )

    dao_data_access = providers.Factory(
        resolve_data_access,
        with_cache=enable_cache,
        scheduler=task_scheduler,
        redis_storage=storage_redis,
        invalidator=cache_invalidator,
        sql_data_access=dao_sqlalchemy,
        ttl=300,
    )

    # --- Composition Root ---
    coordination_root = providers.Factory(
        SqlAlchemyMinioCoordinator,
        transaction=tx_manager,
        storage=storage_minio,
        data_access=dao_data_access,
    )
