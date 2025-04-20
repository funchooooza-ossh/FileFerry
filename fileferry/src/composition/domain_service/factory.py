from typing import Literal

from application.protocols import FileService
from domain.protocols import FilePolicy, UnitOfWork
from domain.services.files.upload_file import UploadFileService
from domain.utils.file_policy import FilePolicyDefault

FileUseCase = Literal["upload", "retrieve"]


class FileServiceFactory:
    @staticmethod
    def create(
        uow: UnitOfWork,
        use_case: FileUseCase,
        policy: FilePolicy = FilePolicyDefault,
    ) -> FileService:
        match use_case:
            case "upload":
                return UploadFileService(uow=uow, file_policy=policy)
            case "retrieve":
                return
            case _:
                raise ValueError(f"Unknown file use case: {use_case}")
