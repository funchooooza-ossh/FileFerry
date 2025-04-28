from dependency_injector import containers, providers

from application.adapter import FileApplicationAdapter


class AdapterContainer(containers.DeclarativeContainer):
    """Контейнер адаптеров."""

    upload_usecase = providers.Dependency()
    retrieve_usecase = providers.Dependency()
    delete_usecase = providers.Dependency()
    update_usecase = providers.Dependency()
    health_usecase = providers.Dependency()

    file_application_adapter = providers.Factory(
        FileApplicationAdapter,
        upload_usecase=upload_usecase,
        retrieve_usecase=retrieve_usecase,
        delete_usecase=delete_usecase,
        update_usecase=update_usecase,
        health_usecase=health_usecase,
    )
