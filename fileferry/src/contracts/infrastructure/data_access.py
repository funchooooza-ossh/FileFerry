# contracts/infrastructure/data_access.py
from typing import Any, Protocol

from domain.models import FileMeta
from shared.types.component_health import ComponentStatus


class DataAccessContract(Protocol):
    """Конракт для доступа к данным."""

    async def get(self, *args: Any, **kwargs: Any) -> Any:
        """Получить объект данных."""
        ...

    async def save(self, *args: Any, **kwargs: Any) -> Any:
        """Сохранить объект данных.."""
        ...

    async def delete(self, *args: Any, **kwargs: Any) -> Any:
        """Удалить объект данных.."""
        ...

    async def update(self, *args: Any, **kwargs: Any) -> Any:
        """Обновить объект данных."""
        ...

    async def healthcheck(self) -> ComponentStatus:
        """Проверка состояни"""
        ...


class FileMetaDataAccessContract(DataAccessContract, Protocol):
    """
    Контракт для доступа к FileMeta.
    """

    async def get(self, file_id: str) -> FileMeta:
        """Получить FileMeta по ID."""
        ...

    async def save(self, file_meta: FileMeta) -> FileMeta:
        """Сохранить FileMeta."""
        ...

    async def delete(self, file_id: str) -> None:
        """Удалить FileMeta по ID."""
        ...

    async def update(self, meta: FileMeta) -> FileMeta:
        """Обновить FileMeta"""
        ...
