from dependency_injector import containers, providers

from composition.containers.adapters import AdapterContainer
from composition.containers.infrastructure import InfrastructureContainer
from composition.containers.usecases import UsecaseContainer
from infrastructure.config.minio import MinioConfig
from infrastructure.config.postgres import PostgresSettings


class ApplicationContainer(containers.DeclarativeContainer):
    """Главный контейнер приложения."""

    wiring_config = containers.WiringConfiguration(
        packages=[
            "composition.di",
        ],
    )

    # --- Config ---
    postgres_settings = providers.Singleton(PostgresSettings)
    minio_settings = providers.Singleton(MinioConfig)
    config = providers.Configuration()

    # --- Infrastructure ---
    infrastructure: providers.Container[InfrastructureContainer] = providers.Container(
        InfrastructureContainer,
        config_postgres=postgres_settings,
        config_minio=minio_settings,
        enable_cache=config.with_cache,
    )

    # --- Usecases ---
    usecases = providers.Container(
        UsecaseContainer,
        coordinator=infrastructure.coordination_root,  # type: ignore
        task_manager=infrastructure.task_exec,  # type: ignore
    )

    # --- Adapters ---
    adapters = providers.Container(
        AdapterContainer,
        upload_usecase=usecases.upload_usecase,  # type: ignore
        retrieve_usecase=usecases.retrieve_usecase,  # type: ignore
        delete_usecase=usecases.delete_usecase,  # type: ignore
        update_usecase=usecases.update_usecase,  # type: ignore
        health_usecase=usecases.health_usecase,  # type: ignore
        snapshot_usecase=usecases.snapshot_usecase,  # type: ignore
    )
