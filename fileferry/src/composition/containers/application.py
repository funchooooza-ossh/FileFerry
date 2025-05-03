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

    # --- Infrastructure ---
    infrastructure: providers.Container[InfrastructureContainer] = providers.Container(
        InfrastructureContainer,
        postgres_config=postgres_settings,
        minio_config=minio_settings,
    )

    # --- Usecases ---
    usecases = providers.Container(
        UsecaseContainer,
        coordinator=infrastructure.atomic_operation,  # type: ignore
    )

    # --- Adapters ---
    adapters = providers.Container(
        AdapterContainer,
        upload_usecase=usecases.upload_usecase,  # type: ignore
        retrieve_usecase=usecases.retrieve_usecase,  # type: ignore
        delete_usecase=usecases.delete_usecase,  # type: ignore
        update_usecase=usecases.update_usecase,  # type: ignore
        health_usecase=usecases.health_usecase,  # type: ignore
    )
