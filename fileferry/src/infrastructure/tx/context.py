from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from contracts.infrastructure import TransactionContextContract
from infrastructure.exceptions.handlers.alchemy_handler import wrap_sqlalchemy_failure


class SqlAlchemyTransactionContext(TransactionContextContract):
    """
    Контекст управления сессией SQLAlchemy, а также объектом session.begin(),
    который являет собой транзакцию (AsyncSessionTransaction).
    Вынесен в отдельный класс, как адаптер для отделения ответственности
    остальных классов за состояние сессии.
    Используется в контексте AtomicOperation для управления сессией внутри DataAccess классов.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._transaction: Optional[AsyncSessionTransaction] = None

    @property
    def session(self) -> AsyncSession:
        if self._transaction is None:
            raise RuntimeError("Attempt to access session before transaction started")
        return self._session

    @wrap_sqlalchemy_failure
    async def begin(self) -> None:
        self._transaction = await self._session.begin()

    @wrap_sqlalchemy_failure
    async def commit(self) -> None:
        if self._transaction is not None:
            await self._transaction.commit()

    @wrap_sqlalchemy_failure
    async def rollback(self) -> None:
        if self._transaction is not None:
            await self._transaction.rollback()

    @wrap_sqlalchemy_failure
    async def close(self) -> None:
        await self._session.close()
