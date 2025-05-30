from typing import cast

from dependency_injector import containers, providers

from composition.containers.adapters import AdapterContainer
from composition.containers.domain import DomainContainer
from composition.containers.infrastructure import InfrastructureContainer
from composition.containers.usecases import UsecaseContainer
from infrastructure.config.minio import MinioConfig
from infrastructure.config.postgres import PostgresSettings
from infrastructure.config.redis import RedisConfig
from shared.config import Settings as AppConfig


class ApplicationContainer(containers.DeclarativeContainer):
    """
    ApplicationContainer (Главный контейнер приложения)

    Этот контейнер является корневым для приложения и отвечает за инициализацию и связывание всех зависимостей.
    Он организован по следующим секциям:

    1. Config (Конфигурация):
        - `config_postgres`: Настройки для PostgreSQL.
        - `config_minio`: Настройки для MinIO.
        - `config_redis`: Настройки для Redis.
        - `config_app`: Общие настройки приложения.

    2. Domain (Домен):
        - `domain`: Контейнер доменных объектов.

    3. Infrastructure (Инфраструктура):
        - `infrastructure`: Контейнер инфраструктурных компонентов, таких как координация, выполнение задач,
          вспомогательные утилиты для работы с файлами и кэширование.

    4. Usecases (Сценарии использования):
        - `usecases`: Контейнер для бизнес-логики приложения, включая сценарии загрузки, извлечения, удаления,
          обновления, проверки состояния и создания снимков.

    5. Adapters (Адаптеры):
        - `adapters`: Контейнер для адаптеров, связывающих сценарии использования с внешними интерфейсами.

    Этот контейнер обеспечивает модульность и удобство управления зависимостями в приложении.
    """

    """Главный контейнер приложения."""

    wiring_config = containers.WiringConfiguration(
        packages=[
            "composition.di",
        ],
    )

    # --- Config ---
    config_postgres = providers.Singleton(PostgresSettings)
    config_minio = providers.Singleton(MinioConfig)
    config_redis = providers.Singleton(RedisConfig)
    config_app = providers.Singleton(AppConfig)

    domain = cast("DomainContainer", providers.Container(DomainContainer))

    # --- Infrastructure ---
    infrastructure = cast(
        "InfrastructureContainer",
        providers.Container(
            InfrastructureContainer,
            config_postgres=config_postgres,
            config_minio=config_minio,
            config_redis=config_redis,
            enable_cache=config_app.provided.cache_enabled,
        ),
    )

    # --- Usecases ---
    usecases = cast(
        "UsecaseContainer",
        providers.Container(
            UsecaseContainer,
            coordination_root=infrastructure.coordination_root,
            task_exec=infrastructure.task_exec,
            file_helper=infrastructure.file_helper,
            default_policy=domain.default_policy,
            meta_factory=domain.meta_factory,
        ),
    )

    # --- Adapters ---
    adapters = cast(
        "AdapterContainer",
        providers.Container(
            AdapterContainer,
            upload_usecase=usecases.upload_usecase,
            retrieve_usecase=usecases.retrieve_usecase,
            delete_usecase=usecases.delete_usecase,
            update_usecase=usecases.update_usecase,
            health_usecase=usecases.health_usecase,
            snapshot_usecase=usecases.snapshot_usecase,
        ),
    )
