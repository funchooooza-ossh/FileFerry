from typing import Optional, Protocol

from contracts.infrastructure.data_access import (
    CacheAsideContract,
    DataAccessContract,
    SQLAlchemyDataAccessContract,
)
from contracts.infrastructure.storage import StorageAccessContract


class AtomicOperationContract(Protocol):
    """Контракт для атомарных операций между базой данных и хранилищем."""

    data_access: DataAccessContract
    storage: StorageAccessContract

    async def __aenter__(self) -> "AtomicOperationContract":
        """Начинает атомарную операцию."""
        ...

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[type[BaseException]],
    ) -> None:
        """Закрывает атомарную операцию: либо фиксируем, либо откатываем."""
        ...

    async def commit(self) -> None:
        """Фиксируем изменения в базе данных и хранилище."""
        ...

    async def rollback(self) -> None:
        """Откатываем изменения в базе данных и хранилище."""
        ...


class SQLAlchemyMinioAtomicContract(AtomicOperationContract, Protocol):
    data_access: CacheAsideContract  # type: ignore override насильно
    storage: StorageAccessContract
    sql_data_access: SQLAlchemyDataAccessContract
