from dataclasses import dataclass
from typing import TypedDict

from domain.models.value_objects import ContentType, FileId, FileName, FileSize
from shared.enums import HealthStatus


@dataclass(slots=True, frozen=True)
class FileMeta:
    id: FileId
    name: FileName
    content_type: ContentType
    size: FileSize

    def as_dict(self) -> dict[str, str | int]:
        return {
            "id": self.id.value,
            "name": self.name.value,
            "content_type": self.content_type.value,
            "size": self.size.value,
        }

    def get_id(self) -> str:
        return self.id.value

    def get_name(self) -> str:
        return self.name.value

    def get_content_type(self) -> str:
        return self.content_type.value

    def get_size(self) -> int:
        return self.size.value


class ComponentStatuses(TypedDict):
    db: bool
    storage: bool


@dataclass(slots=True, frozen=True)
class HealthReport:
    status: HealthStatus
    components: ComponentStatuses

    @classmethod
    def generate(cls, components: ComponentStatuses) -> "HealthReport":
        statuses = [bool(value) for value in components.values()]

        overall_status = HealthStatus.from_boolean(*statuses)

        return cls(status=overall_status, components=components)
