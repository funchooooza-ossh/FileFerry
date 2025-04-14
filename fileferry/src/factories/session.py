from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
    OperationalError,
    ProgrammingError,
    SQLAlchemyError,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from exceptions.repositories import (
    RepositoryError,
    RepositoryIntegrityError,
    RepositoryNotFoundError,
    RepositoryOperationalError,
    RepositoryORMError,
    RepositoryProgrammingError,
)
from settings import settings
from loguru import logger

engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session

        except SQLAlchemyError as exc:
            logger.exception(exc)

            if isinstance(exc, NoResultFound):
                raise RepositoryNotFoundError() from exc

            if isinstance(exc, IntegrityError):
                await session.rollback()
                raise RepositoryIntegrityError from exc

            if isinstance(exc, OperationalError):
                await session.rollback()
                raise RepositoryOperationalError() from exc

            if isinstance(exc, ProgrammingError):
                await session.rollback()
                raise RepositoryProgrammingError() from exc

            await session.rollback()
            raise RepositoryORMError() from exc

        except RepositoryError as exc:
            await session.rollback()
            raise exc

        except Exception as exc:
            logger.exception(exc)
            await session.rollback()
            raise RepositoryError from exc

        else:
            await session.commit()
