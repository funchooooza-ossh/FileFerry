from dataclasses import dataclass
from typing import Optional
from domain.models.enums import FileStatus


@dataclass(slots=True)
class FileMeta:
    id: str
    name: str
    content_type: str
    size: int
    status: Optional[FileStatus]
    reason: Optional[str] = None
