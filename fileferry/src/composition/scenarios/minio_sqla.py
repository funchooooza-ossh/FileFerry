from application.orchestrators.file_adapter import FileAPIAdapter
from composition.meta_factory import create_filemeta
from composition.minio.factory import create_minio_client
from composition.uow.factory import UnitOfWorkFactory
from composition.usecases.factory import (
    RetrieveFileServiceFactory,
    UploadFileServiceFactory,
)
from contracts.composition import DependencyContext, FileAction
from infrastructure.repositories.files.minio_storage import MinioRepository
from infrastructure.utils.file_helper import FileHelper


def bootstrap_minio_sqla(ctx: DependencyContext) -> FileAPIAdapter:
    uow = UnitOfWorkFactory.create(config="sqla")
    file_analyzer = FileHelper()
    client = create_minio_client(_type="default")
    storage = MinioRepository(client=client, bucket_name=ctx.bucket_name)
    match ctx.action:
        case FileAction.UPLOAD:
            service = UploadFileServiceFactory.create(uow=uow, storage=storage)
            return FileAPIAdapter(
                file_analyzer=file_analyzer,
                upload_service=service,
                meta_factory=create_filemeta,
            )
        case FileAction.RETRIEVE:
            service = RetrieveFileServiceFactory.create(uow=uow, storage=storage)
            return FileAPIAdapter(
                file_analyzer=file_analyzer,
                retrieve_service=service,
                meta_factory=create_filemeta,
            )
        case _:
            raise NotImplementedError("Such action not implemented")
