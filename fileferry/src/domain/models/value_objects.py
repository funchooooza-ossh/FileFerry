import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DomainValueObject(ABC):
    _value: Any

    @property
    def value(self) -> Any:
        return self._value

    @abstractmethod
    def __post_init__(self) -> None:
        pass


@dataclass(frozen=True)
class FileId(DomainValueObject):
    def __post_init__(self) -> None:
        try:
            uuid.UUID(self._value)
        except ValueError:
            raise ValueError("Invalid UUID") from None

    @staticmethod
    def new() -> "FileId":
        return FileId(uuid.uuid4().hex)


@dataclass(frozen=True)
class FileName(DomainValueObject):
    def __post_init__(self) -> None:
        if not self._value:
            raise ValueError("File name cannot be empty")
        if len(self._value) > 255:
            raise ValueError("File name too long")
        if "/" in self._value or "\\" in self._value:
            raise ValueError("File name contains illegal characters")


@dataclass(frozen=True)
class ContentType(DomainValueObject):
    def __post_init__(self) -> None:
        if not self._value or "/" not in self._value:
            raise ValueError("Invalid MIME type format")

        main_type, _, sub_type = self._value.partition("/")
        if not main_type or not sub_type:
            raise ValueError("Incomplete MIME type")


@dataclass(frozen=True)
class FileSize(DomainValueObject):
    def __post_init__(self) -> None:
        if self._value <= 0:
            raise ValueError("File size must be positive")
        # if self.value > 10 * 1024 * 1024 * 1024:  # 10 GB, например
        # raise ValueError("File size exceeds maximum allowed limit")
