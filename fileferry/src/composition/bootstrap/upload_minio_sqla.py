from application.services.file import ApplicationFileServiceImpl
from composition.contracts import DependencyContext
from composition.filemeta import create_filemeta
from composition.uow.factory import UnitOfWorkFactory
from composition.upload_service.factory import FileServiceFactory
from infrastructure.utils.file_helper import FileHelper


def bootstrap_minio_sqla(ctx: DependencyContext) -> ApplicationFileServiceImpl:
    uow = UnitOfWorkFactory.create(config="minio-sqla")
    match ctx.action:
        case "upload":
            service = FileServiceFactory.create(uow=uow, use_case="upload")
        case "get":
            return
    file_analyzer = FileHelper()

    return ApplicationFileServiceImpl(
        file_analyzer=file_analyzer,
        service=service,
        meta_factory=create_filemeta,
    )
