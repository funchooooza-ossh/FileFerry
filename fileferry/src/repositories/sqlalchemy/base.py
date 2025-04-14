from typing import Generic, TypeVar, Optional, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from exceptions.repositories import RepositoryORMError


ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseSqlAlchemyRepository(Generic[ModelType]):
    model: Optional[Type[ModelType]] = None

    def __init_subclass__(cls):
        if not cls.model:
            raise TypeError("Subclasses must provide model type")
        return super().__init_subclass__()

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, obj: ModelType) -> None:
        """
        Удобно использовать вместо
        self._session.add(obj)
        """
        self._session.add(obj)

    async def delete(self, obj: ModelType) -> None:
        """
        Аналогично add
        """
        await self._session.delete(obj)

    async def flush(self, *objects: ModelType) -> None:
        """
        Flush куда более атомарно-безопасный вариант,
        отработали с репо, зафлашили,
        в конце жизни сессии извне она закоммитит, если все хорошо.
        """
        await self._session.flush(objects)

    async def commit(self) -> None:
        """
        Хард-коммит изменений. Использовать в крайних случаях.
        Идеально — коммитить снаружи (через UnitOfWork).
        """
        try:
            await self._session.commit()
        except Exception as exc:
            await self._session.rollback()
            raise RepositoryORMError() from exc

    async def rollback(self) -> None:
        """
        Ручной откат изменений, если логика требует досрочного прекращения транзакции.
        """
        await self._session.rollback()
