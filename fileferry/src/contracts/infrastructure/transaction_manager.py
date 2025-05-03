from typing import Protocol

from contracts.infrastructure import TransactionContext


class TransactionManagerContract(Protocol):
    _context: TransactionContext

    async def start(
        self,
    ) -> None: ...

    async def end(self) -> None: ...

    async def apply(self) -> None: ...

    async def reject(self) -> None: ...
