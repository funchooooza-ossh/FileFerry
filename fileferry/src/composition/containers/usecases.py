from dependency_injector import containers, providers

from application.usecases import (
    DeleteUseCase,
    RetrieveUseCase,
    UpdateUseCase,
    UploadUseCase,
)
from domain.models.create_filemeta import create_filemeta
from domain.services.upload_policy import FilePolicyDefault
from infrastructure.utils.file_helper import FileHelper


class UsecaseContainer(containers.DeclarativeContainer):
    """Контейнер юзкейсов приложения."""

    # Зависимости
    atomic = providers.Dependency()
    helper = providers.Singleton(FileHelper)
    policy = providers.Singleton(FilePolicyDefault)
    meta_factory = providers.Object(create_filemeta)

    # Фабрики
    upload_usecase: providers.Factory[UploadUseCase] = providers.Factory(
        UploadUseCase,
        atomic=atomic,
        helper=helper,
        policy=policy,
        meta_factory=meta_factory,
    )

    retrieve_usecase: providers.Factory[RetrieveUseCase] = providers.Factory(
        RetrieveUseCase, atomic=atomic
    )

    delete_usecase: providers.Factory[DeleteUseCase] = providers.Factory(
        DeleteUseCase, atomic=atomic
    )

    update_usecase: providers.Factory[UpdateUseCase] = providers.Factory(
        UpdateUseCase,
        atomic=atomic,
        helper=helper,
        policy=policy,
        meta_factory=meta_factory,
    )
