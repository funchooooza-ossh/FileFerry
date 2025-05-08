from dependency_injector import containers, providers

from domain.models.create_filemeta import create_filemeta
from domain.services.upload_policy import FilePolicyDefault


class DomainContainer(containers.DeclarativeContainer):
    """
    DomainContainer (Контейнер доменного слоя)

    Контейнер для управления зависимостями доменного слоя приложения.
    Содержит провайдеры для создания объектов, связанных с доменной логикой.

    Атрибуты:
        meta_factory (providers.Object): Провайдер для создания объекта метаинформации файла.
        default_policy (providers.Factory): Провайдер для создания объекта политики по умолчанию.
    """

    meta_factory = providers.Object(create_filemeta)
    default_policy = providers.Factory(FilePolicyDefault)
