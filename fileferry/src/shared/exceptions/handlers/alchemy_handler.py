import functools
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar, cast

from loguru import logger
from sqlalchemy.exc import (
    SQLAlchemyError,
)

from shared.exceptions.exc_classes.infrastructure import DataAccessError
from shared.exceptions.mappers.alchemy_errors import SQLAlchemyErrorMapper

logger = logger.bind(name="trace")

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def wrap_sqlalchemy_failure(func: F) -> F:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.trace(f"[ALCHEMY] → {func.__qualname__}()")
        try:
            result = await func(*args, **kwargs)
            logger.info(f"[ALCHEMY][OK] → {func.__qualname__}()")
            return result

        except DataAccessError:
            raise

        except SQLAlchemyError as exc:
            logger.warning(f"[ALCHEMY][ERR] Error in {func.__qualname__}: {exc}")

            raise SQLAlchemyErrorMapper.map_error(exc) from exc
        except RuntimeError as exc:
            logger.critical(
                f"[ALCHEMY][CRITICAL] Runtime error in {func.__qualname__}: {exc}"
            )
            raise DataAccessError from exc
        except Exception as exc:
            logger.exception(f"[ALCHEMY][ERR] Error in {func.__qualname__}: {exc}")
            raise DataAccessError from exc

    return cast("F", wrapper)
