from typing import Literal

from application.services.retrieve_file import RetrieveFileServiceImpl
from application.services.upload_file import UploadFileServiceImpl
from contracts.application import RetrieveFileService, UploadFileService
from contracts.domain import FilePolicy, UnitOfWork
from domain.services.upload_policy import FilePolicyDefault

FileUseCase = Literal["upload", "retrieve"]


class UploadFileServiceFactory:
    @staticmethod
    def create(
        uow: UnitOfWork,
        use_case: FileUseCase,
        policy: FilePolicy = FilePolicyDefault,
    ) -> UploadFileService:
        match use_case:
            case "upload":
                return UploadFileServiceImpl(uow=uow, file_policy=policy)
            case _:
                raise ValueError(f"Unknown file use case: {use_case}")


class RetrieveFileServiceFactory:
    @staticmethod
    def create(uow: UnitOfWork, use_case: FileUseCase) -> RetrieveFileService:
        match use_case:
            case "retrieve":
                return RetrieveFileServiceImpl(uow=uow)
            case _:
                raise ValueError(f"Unknown file use case: {use_case}")
