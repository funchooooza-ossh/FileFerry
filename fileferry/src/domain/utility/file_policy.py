from domain.models.value_objects import ContentType, FileSize


class FilePolicy:
    FORBIDDEN_TYPES = {"application/javascript", "text/html", "application/x-empty"}

    @classmethod
    def is_allowed(cls, mime: ContentType, size: FileSize) -> bool | str:
        if mime.value in cls.FORBIDDEN_TYPES:
            return False
        return not size.value <= 0
