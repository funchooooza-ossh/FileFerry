from dependency_injector import containers, providers

from domain.models.create_filemeta import create_filemeta
from domain.services.upload_policy import FilePolicyDefault


class DomainContainer(containers.DeclarativeContainer):
    """
    Контейнер доменного слоя. Весьма скудный.
    """

    meta_factory = providers.Object(create_filemeta)
    default_policy = providers.Factory(FilePolicyDefault)
