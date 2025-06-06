from typing import Protocol

from contracts.infrastructure import TransactionContextContract


class TransactionManagerContract(Protocol):
    """
    Контракт менеджера транзакции БД.
    Инкапсулирует работу с контекстом транзакции.
    """

    _context: TransactionContextContract

    async def start(
        self,
    ) -> None: ...

    async def end(self) -> None: ...

    async def apply(self) -> None: ...

    async def reject(self) -> None: ...
