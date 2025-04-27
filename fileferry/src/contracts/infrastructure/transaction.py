from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession


class TransactionContext(Protocol):
    session: AsyncSession
    """Контекст управления транзакцией."""

    async def begin(self) -> None: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
