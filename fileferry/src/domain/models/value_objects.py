import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class FileId:
    value: str

    def __post_init__(self) -> None:
        try:
            uuid.UUID(self.value)
        except ValueError:
            raise ValueError("Invalid UUID") from None

    @staticmethod
    def new() -> "FileId":
        return FileId(uuid.uuid4().hex)


@dataclass(frozen=True)
class FileName:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("File name cannot be empty")
        if len(self.value) > 255:
            raise ValueError("File name too long")
        if "/" in self.value or "\\" in self.value:
            raise ValueError("File name contains illegal characters")


@dataclass(frozen=True)
class ContentType:
    value: str

    def __post_init__(self) -> None:
        if not self.value or "/" not in self.value:
            raise ValueError("Invalid MIME type format")

        main_type, _, sub_type = self.value.partition("/")
        if not main_type or not sub_type:
            raise ValueError("Incomplete MIME type")


@dataclass(frozen=True)
class FileSize:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("File size must be positive")
        # if self.value > 10 * 1024 * 1024 * 1024:  # 10 GB, например
        # raise ValueError("File size exceeds maximum allowed limit")
