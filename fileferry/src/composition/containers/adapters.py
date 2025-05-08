from dependency_injector import containers, providers

from application.adapters.crud_adapter import FileApplicationAdapter
from application.adapters.system_adapter import SystemAdapter


class AdapterContainer(containers.DeclarativeContainer):
    """
    AdapterContainer - это контейнер, который предоставляет зависимости и фабрики для адаптеров приложения.

    Атрибуты:
        upload_usecase (Dependency): Зависимость для использования сценария загрузки.
        retrieve_usecase (Dependency): Зависимость для использования сценария получения данных.
        delete_usecase (Dependency): Зависимость для использования сценария удаления.
        update_usecase (Dependency): Зависимость для использования сценария обновления.
        health_usecase (Dependency): Зависимость для использования сценария проверки состояния системы.
        snapshot_usecase (Dependency): Зависимость для использования сценария создания снимков.

    Фабрики:
        crud_adapter (Factory): Фабрика для создания экземпляров FileApplicationAdapter с предоставленными зависимостями.
        system_adapter (Factory): Фабрика для создания экземпляров SystemAdapter с предоставленными зависимостями.
    """

    """Контейнер адаптеров."""

    upload_usecase = providers.Dependency()
    retrieve_usecase = providers.Dependency()
    delete_usecase = providers.Dependency()
    update_usecase = providers.Dependency()
    health_usecase = providers.Dependency()
    snapshot_usecase = providers.Dependency()

    crud_adapter = providers.Factory(
        FileApplicationAdapter,
        upload_usecase=upload_usecase,
        retrieve_usecase=retrieve_usecase,
        delete_usecase=delete_usecase,
        update_usecase=update_usecase,
    )

    system_adapter = providers.Factory(
        SystemAdapter, health_usecase=health_usecase, snapshot_usecase=snapshot_usecase
    )
