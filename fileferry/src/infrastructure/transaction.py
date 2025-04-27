from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from contracts.infrastructure import TransactionContext
from infrastructure.utils.handlers.sqlalchemy_handler import wrap_sqlalchemy_failure


class SqlAlchemyTransactionContext(TransactionContext):
    """Контекст управления транзакцией через SQLAlchemy AsyncSession."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self._transaction: Optional[AsyncSessionTransaction] = None

    @wrap_sqlalchemy_failure
    async def begin(self) -> None:
        self._transaction = await self.session.begin()

    @wrap_sqlalchemy_failure
    async def commit(self) -> None:
        if self._transaction is not None:
            await self._transaction.commit()

    @wrap_sqlalchemy_failure
    async def rollback(self) -> None:
        if self._transaction is not None:
            await self._transaction.rollback()
