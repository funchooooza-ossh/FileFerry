
from application.usecases.retrieve_file import RetrieveFileServiceImpl
from application.usecases.upload_file import UploadFileServiceImpl
from contracts.application import FilePolicy, FileStorage, RetrieveFileService, UnitOfWork, UploadFileService
from domain.services.upload_policy import FilePolicyDefault


class UploadFileServiceFactory:
    @staticmethod
    def create(
        uow: UnitOfWork,
        storage: FileStorage,
        policy: FilePolicy = FilePolicyDefault,
    ) -> UploadFileService:
        return UploadFileServiceImpl(uow=uow, file_policy=policy, storage=storage)


class RetrieveFileServiceFactory:
    @staticmethod
    def create(uow: UnitOfWork, storage: FileStorage) -> RetrieveFileService:
        return RetrieveFileServiceImpl(uow=uow, storage=storage)
