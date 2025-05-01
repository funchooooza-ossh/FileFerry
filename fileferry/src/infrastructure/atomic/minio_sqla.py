from typing import Optional

from contracts.infrastructure import (
    CacheAsideContract,
    SQLAlchemyDataAccessContract,
    SQLAlchemyMinioAtomicContract,
    StorageAccessContract,
    TransactionManagerContract,
)


class SqlAlchemyMinioAtomicOperation(SQLAlchemyMinioAtomicContract):
    def __init__(
        self,
        *,
        sql_data_access: SQLAlchemyDataAccessContract,
        transaction: TransactionManagerContract,
        storage: StorageAccessContract,
        cache_aside: CacheAsideContract,
    ) -> None:
        self._sql_data_access = sql_data_access
        self._transaction = transaction
        self.storage = storage
        self.data_access = cache_aside

    async def __aenter__(self) -> "SqlAlchemyMinioAtomicOperation":
        await self._transaction.start(self._sql_data_access)
        self.data_access.bind_delegate(self._sql_data_access)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[type[BaseException]],
    ) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self._transaction.end()

    async def commit(self) -> None:
        """Фиксация базы данных и staged файлов."""
        if self._transaction:
            await self._transaction.apply()

    async def rollback(self) -> None:
        """Откат базы данных и удаление staged файлов."""
        if self._transaction:
            await self._transaction.reject()
