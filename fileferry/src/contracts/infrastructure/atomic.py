from typing import Optional, Protocol

from contracts.infrastructure.data_access import (
    DataAccessContract,
    SQLAlchemyDataAccessContract,
)
from contracts.infrastructure.storage import StorageAccessContract
from shared.enums import Buckets


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

    async def stage_file(
        self, staged_file_id: str, final_file_id: str, bucket: Buckets
    ) -> None:
        """Добалявем данные измененных файлов в инстанс-список"""
        ...

    def transactional(
        self, transactional: bool = True
    ) -> "AtomicOperationContract": ...


class SQLAlchemyMinioAtomicContract(AtomicOperationContract, Protocol):
    data_access: SQLAlchemyDataAccessContract  # type: ignore override насильно
    storage: StorageAccessContract
