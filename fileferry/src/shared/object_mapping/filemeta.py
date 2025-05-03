from typing import TypedDict

from domain.models import FileMeta
from infrastructure.types import ORMFileMeta


class DTOFileMeta(TypedDict):
    """
    Контракт представления FileMeta
    в сериализованном виде.
    Используется в REST эндпоинтах и Redis
    """

    id: str
    name: str
    content_type: str
    size: int


class FileMetaMapper:
    """
    Mapper-класс представляющий собой реализацию
    "перетекания" Domain модели FileMeta в необходимые для приложения
    форматы и обратно.
    """

    @staticmethod
    def serialize_filemeta(meta: FileMeta) -> DTOFileMeta:
        return DTOFileMeta(
            id=meta.get_id(),
            name=meta.get_name(),
            content_type=meta.get_content_type(),
            size=meta.get_size(),
        )

    @staticmethod
    def deserialize_filemeta(dto_meta: DTOFileMeta) -> FileMeta:
        return FileMeta.from_raw(
            id=dto_meta["id"],
            name=dto_meta["name"],
            size=dto_meta["size"],
            content_type=dto_meta["content_type"],
        )

    @staticmethod
    def filemeta_to_orm(meta: FileMeta) -> ORMFileMeta:
        return ORMFileMeta(
            id=meta.get_id(),
            name=meta.get_name(),
            mime_type=meta.get_content_type(),
            size=meta.get_size(),
        )

    @staticmethod
    def filemeta_from_orm(orm_meta: ORMFileMeta) -> FileMeta:
        return FileMeta.from_raw(
            id=orm_meta["id"],
            name=orm_meta["name"],
            content_type=orm_meta["mime_type"],
            size=orm_meta["size"],
        )
