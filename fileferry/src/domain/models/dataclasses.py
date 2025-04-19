from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class FileMeta:
    id: str
    name: str
    content_type: str
    size: int
