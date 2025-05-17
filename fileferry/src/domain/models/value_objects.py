import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class DomainValueObject(ABC, Generic[T]):
    _value: T

    @property
    def value(self) -> T:
        return self._value

    @abstractmethod
    def __post_init__(self) -> None:  # pragma: no cover
        pass


@dataclass(frozen=True)
class FileId(DomainValueObject[str]):
    def __post_init__(self) -> None:
        try:
            uuid.UUID(self._value)
        except (ValueError, TypeError):
            raise ValueError("Invalid UUID") from None

    @staticmethod
    def new() -> "FileId":
        return FileId(uuid.uuid4().hex)


@dataclass(frozen=True)
class FileName(DomainValueObject[str]):
    _value: str

    def __post_init__(self) -> None:
        if not isinstance(self._value, str) or not self._value.strip():  # type: ignore silly pylance think we cant init dataclass with misstype
            raise ValueError("TypeError or empty string detected.")
        if len(self._value) > 255:
            raise ValueError("File name too long")
        if "/" in self._value or "\\" in self._value:
            raise ValueError("File name contains illegal characters")


@dataclass(frozen=True)
class ContentType(DomainValueObject[str]):
    _value: str

    def __post_init__(self) -> None:
        if not isinstance(self._value, str) or "/" not in self._value:  # type: ignore
            raise ValueError("Invalid MIME type format")

        main_type, _, sub_type = self._value.partition("/")
        if not main_type or not sub_type:
            raise ValueError("Incomplete MIME type")


@dataclass(frozen=True)
class FileSize(DomainValueObject[int]):
    _value: int

    def __post_init__(self) -> None:
        if not isinstance(self._value, int):  # type: ignore
            raise ValueError("File size must be an integer")
        if self._value <= 0:
            raise ValueError("File size must be positive")
