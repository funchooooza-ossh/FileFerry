import functools
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar, cast

from loguru import logger
from miniopy_async.error import S3Error

from infrastructure.exceptions.mappers.infra_errors import InfraErrorMapper
from infrastructure.exceptions.mappers.s3_errors import S3ErrorCode, S3ErrorCodeMapper
from shared.exceptions.infrastructure import StorageError

logger = logger.bind(name="trace")

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def wrap_s3_failure(func: F) -> F:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.trace(f"[S3] → {func.__qualname__}()")
        try:
            result = await func(*args, **kwargs)
            logger.info(f"[S3][OK] → {func.__qualname__}()")
            return result
        except S3Error as exc:
            logger.warning(f"[S3][ERR] Error in {func.__qualname__}: {exc!s}")
            code = (
                S3ErrorCodeMapper.from_string(exc.code)
                if exc.code
                else S3ErrorCode.Unknown
            )
            logger.info(f"ERR CODE: {exc.code} - {code}")
            raise InfraErrorMapper.map_code_to_error(code) from exc
        except Exception as exc:
            logger.exception(f"[S3][ERR] Error in {func.__qualname__}: {exc!s}")
            raise StorageError(f"Unexpected storage error: {exc!s}") from exc

    return cast("F", wrapper)
