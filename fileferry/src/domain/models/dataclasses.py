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
