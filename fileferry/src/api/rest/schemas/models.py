from pydantic import BaseModel

from domain.models.dataclasses import FileMeta


class UploadFileResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, meta: FileMeta) -> "UploadFileResponse":
        return cls(id=meta.id.value, name=meta.name.value)
