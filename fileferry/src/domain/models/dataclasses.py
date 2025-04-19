from dataclasses import dataclass

from domain.models.value_objects import ContentType, FileId, FileName, FileSize


@dataclass(slots=True, frozen=True)
class FileMeta:
    id: FileId
    name: FileName
    content_type: ContentType
    size: FileSize
