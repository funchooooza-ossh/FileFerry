# contracts/infrastructure/data_access.py
from typing import Optional, Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from domain.models import FileMeta


class DataAccessContract(Protocol):
    """Контракт для доступа к данным."""

    async def get(self, file_id: str) -> Optional[FileMeta]:
        """Получить объект данных по ID."""
        ...

    async def save(self, file_meta: FileMeta) -> FileMeta:
        """Сохранить объект данных в хранилище."""
        ...

    async def delete(self, file_id: str) -> None:
        """Удалить объект данных по ID."""
        ...

    async def update(self, meta: FileMeta) -> Optional[FileMeta]:
        """Обновить данные по ID"""
        ...


class SQLAlchemyDataAccessContract(DataAccessContract, Protocol):
    @property
    def session(self) -> AsyncSession: ...

    def bind_session(self, session: AsyncSession) -> None: ...
