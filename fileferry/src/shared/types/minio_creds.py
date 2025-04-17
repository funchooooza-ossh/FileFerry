from typing import TypedDict


class MinioCreds(TypedDict):
    access: str
    secret: str
    endpoint: str
    secure: bool
