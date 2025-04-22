from api.adapter import FileAPIAdapter
from composition.application_service.factory import RetrieveFileServiceFactory, UploadFileServiceFactory
from composition.filemeta import create_filemeta
from composition.uow.factory import UnitOfWorkFactory
from contracts.composition import DependencyContext
from infrastructure.utils.file_helper import FileHelper


def bootstrap_minio_sqla(ctx: DependencyContext) -> FileAPIAdapter:
    uow = UnitOfWorkFactory.create(config="minio-sqla")
    file_analyzer = FileHelper()
    match ctx.action:
        case "upload":
            service = UploadFileServiceFactory.create(uow=uow, use_case="upload")
            return FileAPIAdapter(file_analyzer=file_analyzer, upload_service=service, meta_factory=create_filemeta)
        case "get":
            service = RetrieveFileServiceFactory.create(uow=uow, use_case="retrieve")
            return FileAPIAdapter(file_analyzer=file_analyzer, retrieve_service=service, meta_factory=create_filemeta)
        case _:
            raise NotImplementedError(f"Such action not implemented {_}")
