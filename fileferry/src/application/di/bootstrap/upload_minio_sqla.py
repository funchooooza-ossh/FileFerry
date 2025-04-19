from application.di.filemeta import create_filemeta
from application.di.uow.factory import UnitOfWorkFactory
from application.di.upload_service.factory import FileServiceFactory
from application.services.file import ApplicationFileService
from infrastructure.utils.file_helper import FileHelper


def bootstrap_minio_sqla_upload() -> ApplicationFileService:
    uow = UnitOfWorkFactory.create(config="minio-sqla")
    upload_service = FileServiceFactory.create(uow=uow, use_case="upload")
    file_analyzer = FileHelper()

    return ApplicationFileService(
        file_analyzer=file_analyzer,
        upload_service=upload_service,
        meta_factory=create_filemeta,
    )
