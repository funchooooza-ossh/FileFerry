from contracts.domain import PolicyContract
from domain.models import FileMeta
from shared.exceptions.exc_classes.domain import FilePolicyViolationEror


class FilePolicyDefault(PolicyContract):
    FORBIDDEN_TYPES = {"application/javascript", "text/html", "application/x-empty"}

    @classmethod
    def is_allowed(cls, file_meta: FileMeta) -> bool:
        if (
            file_meta.content_type.value in cls.FORBIDDEN_TYPES
            or file_meta.size.value <= 0
        ):
            raise FilePolicyViolationEror("Невалидный файл")
        return True
