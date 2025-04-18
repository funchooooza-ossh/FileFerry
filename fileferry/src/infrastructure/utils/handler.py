from sqlalchemy.exc import (
    SQLAlchemyError,
    NoResultFound,
    IntegrityError,
    OperationalError,
    ProgrammingError,
)
from shared.exceptions.infrastructure import (
    RepositoryError,
    RepositoryNotFoundError,
    RepositoryIntegrityError,
    RepositoryOperationalError,
    RepositoryProgrammingError,
    RepositoryORMError,
)
import functools
from loguru import logger


def sqlalchemy_handle(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except RepositoryError:
            raise

        except SQLAlchemyError as exc:
            logger.exception(f"[SQLAlchemy] Error in {func.__qualname__}")

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
