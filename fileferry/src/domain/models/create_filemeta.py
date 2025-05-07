from typing import Optional

from domain.models.dataclasses import FileMeta
from domain.models.value_objects import FileId
from shared.exceptions.application import InvalidFileParameters


def create_filemeta(
    file_id: Optional[str], name: str, size: int, content_type: str
) -> FileMeta:
    try:
        file_id = file_id or FileId.new().value
        return FileMeta.from_raw(
            id=file_id, name=name, size=size, content_type=content_type
        )
    except ValueError as exc:
        raise InvalidFileParameters("Unprocessable entity") from exc
