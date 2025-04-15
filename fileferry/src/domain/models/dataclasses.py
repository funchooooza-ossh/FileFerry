from dataclasses import dataclass
from domain.models.enums import FileStatus


@dataclass(slots=True)
class FileMeta:
    id: str
    name: str
    content_type: str
    size: int
    status: FileStatus
