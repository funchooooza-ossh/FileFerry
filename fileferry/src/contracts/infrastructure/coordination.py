from typing import Optional, Protocol

from contracts.infrastructure.data.data_access import (
    FileMetaDataAccessContract,
)
from contracts.infrastructure.data.storage import StorageAccessContract


class OperationCoordinationContract(Protocol):
    """
    Координатор действий для контроля Application слоя
    над работой с базой и хранилищем.
    Проксирует data_access и file_storage наружу.
    Реализует интерфейсы подтверждения изменений и их отката.
    """

    data_access: FileMetaDataAccessContract
    file_storage: StorageAccessContract

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
