from typing import Optional

from contracts.infrastructure import (
    FileMetaDataAccessContract,
    OperationCoordinationContract,
    StorageAccessContract,
    TransactionManagerContract,
)


class SqlAlchemyMinioCoordinator(OperationCoordinationContract):
    """
    Имплементация координатора действий DataAccess и FileStorage.
    Являет собой адаптер инфраструктурных реализаций MiniOStorage и
    любым SQLAlchemy DataAccess.
    В силу особенностей SQLAlchemy также инкапсулирует работу с сессией,
    начиная и завершая её в контексте.
    """

    def __init__(
        self,
        *,
        transaction: TransactionManagerContract,
        storage: StorageAccessContract,
        data_access: FileMetaDataAccessContract,
    ) -> None:
        self._transaction = transaction
        self.file_storage = storage
        self.data_access = data_access

    async def __aenter__(self) -> "SqlAlchemyMinioCoordinator":
        await self._transaction.start()
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
