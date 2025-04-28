from typing import Protocol

from contracts.infrastructure import SQLAlchemyDataAccessContract, TransactionContext


class TransactionManagerContract(Protocol):
    _context: TransactionContext

    async def start(self, *data_accesses: SQLAlchemyDataAccessContract) -> None: ...

    async def end(self) -> None: ...

    async def apply(self) -> None: ...

    async def reject(self) -> None: ...
