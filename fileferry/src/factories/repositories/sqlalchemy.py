from typing import Callable, AsyncGenerator, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.sqlalchemy.base import BaseSqlAlchemyRepository
from utils import SqlAlchemyRegistry
from factories.repositories.base import BaseRepositoryFactory

T_SQLAlchemy = TypeVar("T_SQLAlchemy", bound=BaseSqlAlchemyRepository)


class RepositoryFactory(BaseRepositoryFactory[T_SQLAlchemy]):
    registry = SqlAlchemyRegistry

    def __init__(
        self, session_ctx_factory: Callable[[], AsyncGenerator[AsyncSession, None]]
    ):
        super().__init__(session_ctx_factory)
