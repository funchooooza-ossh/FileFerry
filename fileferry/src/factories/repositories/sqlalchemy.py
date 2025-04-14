from typing import Callable, AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.sqlalchemy.base import BaseSqlAlchemyRepository
from utils import SqlAlchemyRegistry
from factories.repositories.base import BaseRepositoryFactory


class SqlAlchemyFactory(BaseRepositoryFactory[BaseSqlAlchemyRepository]):
    registry = SqlAlchemyRegistry

    def __init__(
        self, session_ctx_factory: Callable[[], AsyncGenerator[AsyncSession, None]]
    ):
        super().__init__(session_ctx_factory)
