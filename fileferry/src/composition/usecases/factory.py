from application.usecases.delete_file import DeleteFileServiceImpl
from application.usecases.healthcheck import HealthCheckServiceImpl
from application.usecases.retrieve_file import RetrieveFileServiceImpl
from application.usecases.upload_file import UploadFileServiceImpl
from contracts.application import (
    DeleteFileService,
    FilePolicy,
    FileStorage,
    HealthCheckService,
    RetrieveFileService,
    UnitOfWork,
    UploadFileService,
)
from domain.services.upload_policy import FilePolicyDefault


class UploadFileServiceFactory:
    @staticmethod
    def create(
        uow: UnitOfWork,
        storage: FileStorage,
        policy: FilePolicy = FilePolicyDefault(),
    ) -> UploadFileService:
        return UploadFileServiceImpl(uow=uow, file_policy=policy, storage=storage)


class RetrieveFileServiceFactory:
    @staticmethod
    def create(uow: UnitOfWork, storage: FileStorage) -> RetrieveFileService:
        return RetrieveFileServiceImpl(uow=uow, storage=storage)


class DeleteFileServiceFactory:
    @staticmethod
    def create(uow: UnitOfWork, storage: FileStorage) -> DeleteFileService:
        return DeleteFileServiceImpl(uow=uow, storage=storage)


class HealthCheckServiceFactory:
    @staticmethod
    def create(uow: UnitOfWork, storage: FileStorage) -> HealthCheckService:
        return HealthCheckServiceImpl(uow=uow, storage=storage)
