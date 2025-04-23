from collections.abc import AsyncGenerator, Callable
from typing import Any, Literal

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db.session import get_async_session
from infrastructure.uow.sqlalchemy import SQLAlchemyUnitOfWork

KnownUoW = Literal["sqla", "mongo"]


class UnitOfWorkFactory:
    @classmethod
    def create(cls, config: KnownUoW, **kwargs: Any) -> Callable:
        match config:
            case "sqla":
                return cls.create_sqlalchemy(**kwargs)
            case "mongo":
                return
            case _:
                raise ValueError("Unknown UoW")

    @staticmethod
    def create_sqlalchemy(
        session_factory: AsyncGenerator[AsyncSession, None] = get_async_session,
    ) -> SQLAlchemyUnitOfWork:
        return SQLAlchemyUnitOfWork(
            session_factory=session_factory,
        )
