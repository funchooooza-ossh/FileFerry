from typing import Optional

from domain.models.dataclasses import FileMeta
from domain.models.value_objects import ContentType, FileId, FileName, FileSize
from shared.exceptions.application import InvalidFileParameters


def create_filemeta(
    file_id: Optional[str], name: str, size: int, content_type: str
) -> FileMeta:
    try:
        id_vo = FileId(file_id) if file_id else FileId.new()
        name_vo = FileName(name)
        ctype_vo = ContentType(content_type)
        size_vo = FileSize(size)

        return FileMeta(id_vo, name_vo, ctype_vo, size_vo)
    except ValueError as exc:
        raise InvalidFileParameters("Unprocessable entity") from exc
