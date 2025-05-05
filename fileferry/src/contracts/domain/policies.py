from typing import Protocol

from domain.models import FileMeta


class PolicyContract(Protocol):
    @classmethod
    def is_allowed(cls, file_meta: FileMeta) -> bool: ...
