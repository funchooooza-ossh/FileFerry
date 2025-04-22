from contracts.application import FilePolicy
from domain.models.value_objects import ContentType, FileSize
from shared.exceptions.domain import FilePolicyViolationEror


class FilePolicyDefault(FilePolicy):
    FORBIDDEN_TYPES = {"application/javascript", "text/html", "application/x-empty"}

    @classmethod
    def is_allowed(cls, mime: ContentType, size: FileSize) -> bool:
        if mime.value in cls.FORBIDDEN_TYPES or size.value <= 0:
            raise FilePolicyViolationEror("Невалидный файл")
        return True
