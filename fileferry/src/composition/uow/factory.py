from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import Any, Literal

from sqlalchemy.ext.asyncio import AsyncSession

from contracts.application import UnitOfWork
from infrastructure.db.session import get_async_session
from infrastructure.uow.sqlalchemy_file import SQLAlchemyUnitOfWork

KnownUoW = Literal["sqla", "mongo"]


class UnitOfWorkFactory:
    @classmethod
    def create(cls, config: KnownUoW, **kwargs: Any) -> UnitOfWork:
        match config:
            case "sqla":
                return cls.create_sqlalchemy(**kwargs)
            case "mongo":
                raise NotImplementedError("Mongo not implemented")
            case _:
                raise ValueError("Unknown UoW")

    @staticmethod
    def create_sqlalchemy(
        session_factory: Callable[[], AbstractAsyncContextManager[AsyncSession]] = get_async_session,
    ) -> SQLAlchemyUnitOfWork:
        return SQLAlchemyUnitOfWork(
            session_factory=session_factory,
        )
