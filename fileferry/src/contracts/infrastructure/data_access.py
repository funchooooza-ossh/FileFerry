# contracts/infrastructure/data_access.py
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from domain.models import FileMeta
from shared.types.component_health import ComponentStatus


class DataAccessContract(Protocol):
    """Контракт для доступа к данным."""

    async def get(self, file_id: str) -> FileMeta:
        """Получить объект данных по ID."""
        ...

    async def save(self, file_meta: FileMeta) -> FileMeta:
        """Сохранить объект данных в хранилище."""
        ...

    async def delete(self, file_id: str) -> None:
        """Удалить объект данных по ID."""
        ...

    async def update(self, meta: FileMeta) -> FileMeta:
        """Обновить данные по ID"""
        ...

    async def healthcheck(self) -> ComponentStatus: ...


class SQLAlchemyDataAccessContract(DataAccessContract, Protocol):
    @property
    def session(self) -> AsyncSession: ...

    def bind_session(self, session: AsyncSession) -> None: ...
