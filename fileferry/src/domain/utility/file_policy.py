class FilePolicy:
    FORBIDDEN_TYPES = {"application/javascript", "text/html", "application/x-empty"}

    @classmethod
    def is_allowed(cls, mime: str) -> bool | str:
        if mime in cls.FORBIDDEN_TYPES:
            return False
        return mime
