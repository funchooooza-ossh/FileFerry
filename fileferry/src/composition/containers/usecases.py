from dependency_injector import containers, providers

from application.usecases import (
    DeleteUseCase,
    HealthCheckUseCase,
    RetrieveUseCase,
    SnapShotUseCase,
    UpdateUseCase,
    UploadUseCase,
)


class UsecaseContainer(containers.DeclarativeContainer):
    """Контейнер юзкейсов приложения."""

    # Зависимости
    coordination_root = providers.Dependency()
    task_exec = providers.Dependency()
    file_helper = providers.Dependency()
    default_policy = providers.Dependency()
    meta_factory = providers.Dependency()

    # Фабрики
    upload_usecase: providers.Factory[UploadUseCase] = providers.Factory(
        UploadUseCase,
        coordinator=coordination_root,
        helper=file_helper,
        policy=default_policy,
        meta_factory=meta_factory,
    )

    retrieve_usecase: providers.Factory[RetrieveUseCase] = providers.Factory(
        RetrieveUseCase, coordinator=coordination_root
    )

    delete_usecase: providers.Factory[DeleteUseCase] = providers.Factory(
        DeleteUseCase, coordinator=coordination_root
    )

    update_usecase: providers.Factory[UpdateUseCase] = providers.Factory(
        UpdateUseCase,
        coordinator=coordination_root,
        helper=file_helper,
        policy=default_policy,
        meta_factory=meta_factory,
    )
    health_usecase: providers.Factory[HealthCheckUseCase] = providers.Factory(
        HealthCheckUseCase, coordinator=coordination_root
    )
    snapshot_usecase: providers.Factory[SnapShotUseCase] = providers.Factory(
        SnapShotUseCase, manager=task_exec
    )
