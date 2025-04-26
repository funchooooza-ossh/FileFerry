import uuid
from typing import AsyncIterator, TypeVar

from domain.models.dataclasses import FileMeta
from domain.models.value_objects import ContentType, FileId, FileName, FileSize

T = TypeVar("T")


class aiter:
    def __init__(self, items: list[T]):
        self._items = iter(items)

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        try:
            return next(self._items)
        except StopIteration:
            raise StopAsyncIteration


def create_filemeta(file_id: FileId | None = None) -> FileMeta:
    new_id = file_id if file_id else FileId(uuid.uuid4().hex)
    size = FileSize(123)
    filename = FileName("test_name")
    content_type = ContentType("application/pdf")

    return FileMeta(id=new_id, name=filename, size=size, content_type=content_type)
