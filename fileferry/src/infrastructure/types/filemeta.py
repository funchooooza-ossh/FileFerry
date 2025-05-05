from typing import TypedDict


class ORMFileMeta(TypedDict):
    """
    Контракт представления FileMeta в ORM
    """

    id: str
    name: str
    mime_type: str
    size: int
