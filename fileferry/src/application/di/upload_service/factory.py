from typing import Literal

from application.protocols import FileService
from domain.protocols import UnitOfWork
from domain.services.files.upload_file import UploadFileService

FileUseCase = Literal["upload", "retrieve"]


class FileServiceFactory:
    @staticmethod
    def create(
        uow: UnitOfWork,
        use_case: FileUseCase,
    ) -> FileService:
        match use_case:
            case "upload":
                return UploadFileService(uow)
            case "retrieve":
                return
            case _:
                raise ValueError(f"Unknown file use case: {use_case}")
