from contracts.infrastructure import (
    TransactionContext,
    TransactionManagerContract,
)


class TransactionManager(TransactionManagerContract):
    """
    Менеджер транзакции БД.
    Инкапсулирует работу с контекстом транзакции.
    """

    def __init__(self, context: TransactionContext) -> None:
        self._context = context
        self._started = False

    async def start(self) -> None:
        if self._started:
            raise RuntimeError("Transaction has already been started")
        await self._context.begin()
        self._started = True

    async def end(self) -> None:
        if not self._started:
            return
        await self._context.close()

    async def apply(self) -> None:
        if not self._started:
            return
        await self._context.commit()

    async def reject(self) -> None:
        if not self._started:
            return
        await self._context.rollback()
