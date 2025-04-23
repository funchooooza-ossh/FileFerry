from typing import Optional, AsyncIterator
from shared.exceptions.infrastructure import InfrastructureError
from domain.models.dataclasses import FileMeta


class FakeUoW:
    def __init__(self, fail: bool = False, fail_unexpected: bool = False):
        self._fail = fail
        self._fail_unexpected = fail_unexpected
        self.committed = False
        self.rolled_back = False
        self.saved_meta: Optional[FileMeta] = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        pass

    async def save(self, meta: FileMeta, stream: AsyncIterator[bytes]) -> None:
        if self._fail_unexpected:
            raise Exception("Unexpected error")
        if self._fail:
            raise InfrastructureError("fail")
        self.saved_meta = meta

    async def commit(self) -> None:
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True
