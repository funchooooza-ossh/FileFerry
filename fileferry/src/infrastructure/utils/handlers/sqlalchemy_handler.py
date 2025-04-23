import functools
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from loguru import logger
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
    OperationalError,
    ProgrammingError,
    SQLAlchemyError,
)

from shared.exceptions.infrastructure import (
    RepositoryError,
    RepositoryIntegrityError,
    RepositoryNotFoundError,
    RepositoryOperationalError,
    RepositoryORMError,
    RepositoryProgrammingError,
)

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def wrap_sqlalchemy_failure(func: F) -> Callable[..., Awaitable[Any]]:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)

        except RepositoryError:
            raise

        except SQLAlchemyError as exc:
            logger.warning(f"[SQLAlchemy] Error in {func.__qualname__}")

            if isinstance(exc, NoResultFound):
                raise RepositoryNotFoundError() from exc

            if isinstance(exc, IntegrityError):
                raise RepositoryIntegrityError() from exc

            if isinstance(exc, OperationalError):
                raise RepositoryOperationalError() from exc

            if isinstance(exc, ProgrammingError):
                raise RepositoryProgrammingError() from exc

            raise RepositoryORMError() from exc

        except Exception as exc:
            logger.exception(f"[Unexpected] Error in {func.__qualname__}")
            raise RepositoryError from exc

    return wrapper
