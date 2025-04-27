from typing import Optional

from contracts.infrastructure import (
    SQLAlchemyDataAccessContract,
    SQLAlchemyMinioAtomicContract,
    StorageAccessContract,
    TransactionContext,
)
from shared.enums import Buckets


class SqlAlchemyMinioAtomicOperation(SQLAlchemyMinioAtomicContract):
    """
    Класс-посредник между слоем приложения и инфраструктурой.
    Проксирует DataAccessObject и Storage в UseCase.
    На себя берет атомарность БД и Хранилища.
    Работает с Transaction контекстом для контроля состояния сессии внутри DataAccess.
    Имеет help-функцию transactinonal(arg:bool=True), чтобы не пытаться откатывать и коммитить
    изменения там, где их изначально не было.
    """

    def __init__(
        self,
        data_access: SQLAlchemyDataAccessContract,
        transaction: TransactionContext,
        storage: StorageAccessContract,
        transactional: bool = True,
    ) -> None:
        self._transaction = transaction
        self.data_access = data_access
        self.storage = storage
        self._transactional = transactional
        self._staged_files: list[tuple[str, str, Buckets]] = (
            []
        )  # (staged_file_id, final_file_id, bucket)

    async def __aenter__(self) -> "SqlAlchemyMinioAtomicOperation":
        await self._transaction.begin()
        self.data_access.bind_session(self._transaction.session)
        return self

    def transactional(
        self, transactional: bool = True
    ) -> "SqlAlchemyMinioAtomicOperation":
        self._transactional = transactional
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[type[BaseException]],
    ) -> None:
        if exc_type and self._transactional:
            await self.rollback()
        else:
            if self._transactional:
                await self.commit()
        await self._transaction.close()

    async def stage_file(
        self, staged_file_id: str, final_file_id: str, bucket: Buckets
    ) -> None:
        """Добавляем staged-файл в список для дальнейшего подтверждения."""
        self._staged_files.append((staged_file_id, final_file_id, bucket))

    async def commit(self) -> None:
        """Фиксация базы данных и staged файлов."""
        if self._transaction:
            await self._transaction.commit()
        if self._staged_files:
            for staged_file_id, final_file_id, bucket in self._staged_files:
                await self.storage.commit(
                    staged_file_id=staged_file_id,
                    final_file_id=final_file_id,
                    bucket=bucket,
                )

    async def rollback(self) -> None:
        """Откат базы данных и удаление staged файлов."""
        if self._transaction:
            await self._transaction.rollback()
        if self._staged_files:
            for staged_file_id, _, bucket in self._staged_files:
                await self.storage.rollback(
                    staged_file_id=staged_file_id,
                    bucket=bucket,
                )
