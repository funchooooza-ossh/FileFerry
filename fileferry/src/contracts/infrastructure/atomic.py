from typing import Optional, Protocol

from contracts.infrastructure.data_access import (
    DataAccessContract,
    SQLAlchemyDataAccessContract,
)
from contracts.infrastructure.storage import StorageAccessContract


class OperationCoordinationContract(Protocol):
    """Контракт для атомарных операций между базой данных и хранилищем."""

    data_access: DataAccessContract
    storage: StorageAccessContract

    async def __aenter__(self) -> "OperationCoordinationContract":
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


class SQLAlchemyMinioCoordinationContract(OperationCoordinationContract, Protocol):
    data_access: DataAccessContract
    storage: StorageAccessContract
    sql_data_access: SQLAlchemyDataAccessContract
