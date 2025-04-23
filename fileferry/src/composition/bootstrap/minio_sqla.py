from application.orchestrators.adapter import FileAPIAdapter
from composition.application_service.factory import RetrieveFileServiceFactory, UploadFileServiceFactory
from composition.filemeta import create_filemeta
from composition.minio.factory import create_minio_client
from composition.uow.factory import UnitOfWorkFactory
from contracts.composition import DependencyContext
from infrastructure.repositories.files.minio import MinioRepository
from infrastructure.utils.file_helper import FileHelper


def bootstrap_minio_sqla(ctx: DependencyContext) -> FileAPIAdapter:
    uow = UnitOfWorkFactory.create(config="sqla")
    file_analyzer = FileHelper()
    client = create_minio_client(_type="default")
    storage = MinioRepository(client=client, bucket_name=ctx.bucket_name)
    match ctx.action:
        case "upload":
            service = UploadFileServiceFactory.create(uow=uow, use_case="upload", storage=storage)
            return FileAPIAdapter(file_analyzer=file_analyzer, upload_service=service, meta_factory=create_filemeta)
        case "get":
            service = RetrieveFileServiceFactory.create(uow=uow, use_case="retrieve", storage=storage)
            return FileAPIAdapter(file_analyzer=file_analyzer, retrieve_service=service, meta_factory=create_filemeta)
        case _:
            raise NotImplementedError(f"Such action not implemented {_}")
