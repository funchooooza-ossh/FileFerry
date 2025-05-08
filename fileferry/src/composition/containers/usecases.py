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
    """
    Класс UsecaseContainer предоставляет контейнер для управления зависимостями и фабриками различных вариантов использования (use cases).

    Атрибуты:
        coordination_root (providers.Dependency): Зависимость, представляющая корневой координатор.
        task_exec (providers.Dependency): Зависимость, представляющая менеджер задач.
        file_helper (providers.Dependency): Зависимость, предоставляющая вспомогательные функции для работы с файлами.
        default_policy (providers.Dependency): Зависимость, представляющая политику по умолчанию.
        meta_factory (providers.Dependency): Зависимость, предоставляющая фабрику метаданных.

    Фабрики:
        upload_usecase (providers.Factory[UploadUseCase]): Фабрика для создания экземпляров UploadUseCase.
        retrieve_usecase (providers.Factory[RetrieveUseCase]): Фабрика для создания экземпляров RetrieveUseCase.
        delete_usecase (providers.Factory[DeleteUseCase]): Фабрика для создания экземпляров DeleteUseCase.
        update_usecase (providers.Factory[UpdateUseCase]): Фабрика для создания экземпляров UpdateUseCase.
        health_usecase (providers.Factory[HealthCheckUseCase]): Фабрика для создания экземпляров HealthCheckUseCase.
        snapshot_usecase (providers.Factory[SnapShotUseCase]): Фабрика для создания экземпляров SnapShotUseCase.
    """

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
