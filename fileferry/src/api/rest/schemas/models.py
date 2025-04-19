from typing import Optional

from pydantic import BaseModel

from domain.models.dataclasses import FileMeta
from domain.models.enums import FileStatus


class UploadFileResponse(BaseModel):
    id: str
    name: str
    status: FileStatus
    reason: Optional[str]

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, meta: FileMeta) -> "UploadFileResponse":
        return cls(id=meta.id, name=meta.name)
