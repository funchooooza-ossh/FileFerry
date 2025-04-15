from magic import Magic


class FilePolicy:
    FORBIDDEN_TYPES = {"application/javascript", "text/html"}

    @classmethod
    def is_allowed(cls, data: bytes) -> bool | str:
        mime = Magic(mime=True).from_buffer(buf=data)
        if mime in cls.FORBIDDEN_TYPES:
            return False
        return mime
