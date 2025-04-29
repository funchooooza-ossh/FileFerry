from dataclasses import dataclass

from domain.models.mixin import AsDictMixin
from domain.models.value_objects import ContentType, FileId, FileName, FileSize
from shared.enums import HealthStatus


@dataclass(slots=True, frozen=True)
class FileMeta(AsDictMixin):
    _id: FileId
    _name: FileName
    _content_type: ContentType
    _size: FileSize
    __asdict_fields__ = ("_id", "_name", "_content_type", "_size")

    def get_id(self) -> str:
        return self._id.value

    def get_name(self) -> str:
        return self._name.value

    def get_content_type(self) -> str:
        return self._content_type.value

    def get_size(self) -> int:
        return self._size.value


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
