from typing import Literal

from application.usecases.retrieve_file import RetrieveFileServiceImpl
from application.usecases.upload_file import UploadFileServiceImpl
from contracts.api import RetrieveFileService, UploadFileService
from contracts.application import FilePolicy, FileStorage, UnitOfWork
from domain.services.upload_policy import FilePolicyDefault

FileUseCase = Literal["upload", "retrieve"]


class UploadFileServiceFactory:
    @staticmethod
    def create(
        uow: UnitOfWork,
        use_case: FileUseCase,
        storage: FileStorage,
        policy: FilePolicy = FilePolicyDefault,
    ) -> UploadFileService:
        match use_case:
            case "upload":
                return UploadFileServiceImpl(uow=uow, file_policy=policy, storage=storage)
            case _:
                raise ValueError(f"Unknown file use case: {use_case}")


class RetrieveFileServiceFactory:
    @staticmethod
    def create(uow: UnitOfWork, use_case: FileUseCase, storage: FileStorage) -> RetrieveFileService:
        match use_case:
            case "retrieve":
                return RetrieveFileServiceImpl(uow=uow, storage=storage)
            case _:
                raise ValueError(f"Unknown file use case: {use_case}")
