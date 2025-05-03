from dataclasses import dataclass

from domain.models.value_objects import ContentType, FileId, FileName, FileSize
from shared.enums import HealthStatus


@dataclass(slots=True, frozen=True)
class FileMeta:
    _id: FileId
    _name: FileName
    _content_type: ContentType
    _size: FileSize

    def get_id(self) -> str:
        return self._id.value

    def get_name(self) -> str:
        return self._name.value

    def get_content_type(self) -> str:
        return self._content_type.value

    def get_size(self) -> int:
        return self._size.value

    @classmethod
    def from_raw(cls, id: str, name: str, content_type: str, size: int) -> "FileMeta":
        return cls(
            _id=FileId(id),
            _name=FileName(name),
            _content_type=ContentType(content_type),
            _size=FileSize(size),
        )


@dataclass(frozen=True)
class ComponentStatuses:
    db: bool
    storage: bool


@dataclass(slots=True, frozen=True)
class HealthReport:
    status: HealthStatus
    components: ComponentStatuses

    @classmethod
    def generate(cls, components: ComponentStatuses) -> "HealthReport":
        statuses = [components.db and components.storage]

        overall_status = HealthStatus.from_boolean(*statuses)

        return cls(status=overall_status, components=components)
