from typing import ClassVar

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
from infrastructure.coordination.minio_sqla import SqlAlchemyMinioCoordinator
from infrastructure.utils.file_helper import FileHelper


class InfrastructureContainer(containers.DeclarativeContainer):
    """
    Класс InfrastructureContainer представляет собой декларативный контейнер для управления зависимостями
    и конфигурацией инфраструктуры приложения. Он использует библиотеку dependency-injector для определения
    и предоставления различных компонентов, таких как базы данных, клиенты, хранилища и задачи.

    Атрибуты:
        config_postgres: Конфигурация для подключения к PostgreSQL.
        config_minio: Конфигурация для клиента MinIO.
        config_redis: Конфигурация для клиента Redis.
        enable_cache: Флаг, указывающий, включено ли кэширование.

    Клиенты:
        engine_postgres: Singleton для создания SQLAlchemy Engine с использованием конфигурации PostgreSQL.
        sessionmaker_postgres: Singleton для создания фабрики сессий SQLAlchemy.
        session_factory: Factory для создания сессий базы данных.
        client_minio: Singleton для создания клиента MinIO.
        client_redis: Singleton для создания клиента Redis с поддержкой кэширования.

    Транзакционный слой:
        tx_context: ContextLocalSingleton для управления контекстом транзакций.
        tx_manager: Factory для создания менеджера транзакций.
        dao_sqlalchemy: Factory для создания объекта доступа к данным с использованием SQLAlchemy.

    Задачи:
        task_exec: Singleton для управления задачами с поддержкой кэширования.
        task_scheduler: Singleton для выполнения задач в режиме fire-and-forget.

    Хранилища:
        storage_minio: Factory для создания хранилища MinIO.
        storage_redis: Factory для создания Redis-хранилища с поддержкой кэширования.
        cache_invalidator: Factory для создания объекта, отвечающего за инвалидирование кэша.

    Доступ к данным:
        dao_data_access: Factory для разрешения доступа к данным с поддержкой кэширования,
                         планировщика задач, Redis-хранилища и SQLAlchemy.

    Корень композиции:
        coordination_root: Factory для создания координатора, который объединяет транзакции,
                           хранилище и доступ к данным.

    Вспомогательные компоненты:
        file_helper: Factory для создания вспомогательного объекта FileHelper.
    """

    # --- Configs ---
    config_postgres = providers.Configuration()
    config_minio = providers.Configuration()
    config_redis = providers.Configuration()
    enable_cache = providers.Configuration()

    # --- Clients ---
    engine_postgres = providers.Singleton(
        create_db_engine,
        url=config_postgres.provided.url,
        echo=config_postgres.provided.echo,
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
        prefix=config_redis.provided.cache_prefix,
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
        ttl=config_redis.provided.cache_ttl,
    )

    # --- Composition Root ---
    coordination_root = providers.Factory(
        SqlAlchemyMinioCoordinator,
        transaction=tx_manager,
        storage=storage_minio,
        data_access=dao_data_access,
    )

    # --- Helpers ---
    file_helper: ClassVar[providers.Factory[FileHelper]] = providers.Factory(FileHelper)
