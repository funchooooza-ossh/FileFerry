import functools
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar, cast

from loguru import logger
from miniopy_async.error import S3Error

from infrastructure.enums.s3_errors import map_s3_error
from shared.exceptions.infrastructure import StorageError

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def wrap_s3_failure(
    func: F,
) -> F:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except S3Error as exc:
            logger.warning(f"[S3] Error in {func.__qualname__} ")
            raise map_s3_error(exc) from exc
        except Exception as exc:
            logger.exception(f"[S3] Error in {func.__qualname__} ")
            raise StorageError(f"Unexpected storage error: {exc}") from exc

    return cast("F", wrapper)
