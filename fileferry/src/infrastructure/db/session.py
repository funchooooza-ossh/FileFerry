from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from loguru import logger
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
    OperationalError,
    ProgrammingError,
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from infrastructure.config.db import pg_settings
from shared.config import settings
from shared.exceptions.infrastructure import (
    RepositoryError,
    RepositoryIntegrityError,
    RepositoryNotFoundError,
    RepositoryOperationalError,
    RepositoryORMError,
    RepositoryProgrammingError,
)

engine = create_async_engine(pg_settings.url, echo=settings.app_debug)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор сессий, по большей части заточен под использование внутри своего же блока.
    Реализовал его по принципу "лишним не будет" но вряд ли он будет использоваться так.
    Потому что я решил реализовывать UnitOfWork
    """
    try:
        async with async_session_maker() as session:
            yield session

    except SQLAlchemyError as exc:
        logger.exception(exc)

        if isinstance(exc, NoResultFound):
            raise RepositoryNotFoundError() from exc

        if isinstance(exc, IntegrityError):
            raise RepositoryIntegrityError from exc

        if isinstance(exc, OperationalError):
            raise RepositoryOperationalError() from exc

        if isinstance(exc, ProgrammingError):
            raise RepositoryProgrammingError() from exc

        raise RepositoryORMError() from exc

    except RepositoryError as exc:
        raise exc

    except Exception as exc:
        logger.exception(exc)
        raise RepositoryError from exc
