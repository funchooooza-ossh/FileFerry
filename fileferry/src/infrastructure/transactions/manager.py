from contracts.infrastructure import (
    SQLAlchemyDataAccessContract,
    TransactionContext,
    TransactionManagerContract,
)


class TransactionManager(TransactionManagerContract):
    def __init__(self, context: TransactionContext) -> None:
        self._context = context
        self._bound_data_accesses: list[SQLAlchemyDataAccessContract] = []
        self._started = False

    async def start(self, *data_accesses: SQLAlchemyDataAccessContract) -> None:
        if self._started:
            raise RuntimeError("Transaction has already been started")
        await self._context.begin()
        [
            data_access.bind_session(session=self._context.session)
            for data_access in data_accesses
        ]
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
