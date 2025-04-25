from application.orchestrators.delete_file_adapter import DeleteFileAPIAdapter
from application.orchestrators.retrieve_file_adapter import RetrieveFileAPIAdapter
from application.orchestrators.upload_file_adapter import UploadFileAPIAdapter
from composition.meta_factory import create_filemeta
from composition.minio.factory import create_minio_client
from composition.uow.factory import UnitOfWorkFactory
from composition.usecases.factory import (
    DeleteFileServiceFactory,
    RetrieveFileServiceFactory,
    UploadFileServiceFactory,
)
from contracts.composition import DependencyContext, FileAction, FileAPIAdapterContract
from infrastructure.repositories.files.minio_storage import MinioRepository
from infrastructure.utils.file_helper import FileHelper


def bootstrap_minio_sqla(ctx: DependencyContext) -> FileAPIAdapterContract:
    uow = UnitOfWorkFactory.create(config="sqla")
    file_analyzer = FileHelper()
    client = create_minio_client(_type="default")
    storage = MinioRepository(client=client, bucket_name=ctx.bucket_name)
    match ctx.action:
        case FileAction.UPLOAD:
            service = UploadFileServiceFactory.create(uow=uow, storage=storage)
            return UploadFileAPIAdapter(
                file_analyzer=file_analyzer,
                upload_service=service,
                meta_factory=create_filemeta,
            )
        case FileAction.RETRIEVE:
            service = RetrieveFileServiceFactory.create(uow=uow, storage=storage)
            return RetrieveFileAPIAdapter(
                retrieve_service=service,
            )
        case FileAction.DELETE:
            service = DeleteFileServiceFactory.create(uow=uow, storage=storage)
            return DeleteFileAPIAdapter(delete_service=service)
        case _:
            raise NotImplementedError("Such action not implemented")
