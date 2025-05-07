from contracts.domain import PolicyContract
from domain.models import FileMeta
from shared.exceptions.domain import FilePolicyViolationError


class FilePolicyDefault(PolicyContract):
    FORBIDDEN_TYPES = {"application/javascript", "text/html", "application/x-empty"}

    @classmethod
    def is_allowed(cls, file_meta: FileMeta) -> bool:
        if (
            file_meta.get_content_type() in cls.FORBIDDEN_TYPES
            or file_meta.get_size() <= 0
        ):
            raise FilePolicyViolationError("Невалидный файл")
        return True
