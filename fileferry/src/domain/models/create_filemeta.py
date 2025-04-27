from domain.models.dataclasses import FileMeta
from domain.models.value_objects import ContentType, FileId, FileName, FileSize
from shared.exceptions.exc_classes.application import InvalidFileParameters


def create_filemeta(name: str, size: int, content_type: str) -> FileMeta:
    try:
        id_vo = FileId.new()
        name_vo = FileName(name)
        ctype_vo = ContentType(content_type)
        size_vo = FileSize(size)

        return FileMeta(id=id_vo, name=name_vo, content_type=ctype_vo, size=size_vo)
    except ValueError as exc:
        raise InvalidFileParameters("Unprocessable entity") from exc
