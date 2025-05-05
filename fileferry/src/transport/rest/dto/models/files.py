from pydantic import BaseModel

from domain.models.dataclasses import FileMeta
from shared.object_mapping.filemeta import FileMetaMapper


class UploadFileResponse(BaseModel):
    id: str
    name: str
    size: int
    content_type: str

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, meta: FileMeta) -> "UploadFileResponse":
        return cls.model_validate(FileMetaMapper.serialize_filemeta(meta))


class DeleteFileResponse(BaseModel):
    msg: str

    @classmethod
    def success(cls) -> "DeleteFileResponse":
        return cls(msg="Requested to delete file deleted successfully")
