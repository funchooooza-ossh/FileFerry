import functools
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar, cast

from loguru import logger
from redis.exceptions import ConnectionError, RedisError, TimeoutError

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def wrap_redis_failure(operation: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = args[1] if len(args) > 1 else "<unknown>"
            try:
                return await func(*args, **kwargs)
            except (ConnectionError, TimeoutError) as exc:
                logger.error(
                    f"[REDIS][{operation.upper()}][{key}] Connection error: {exc}"
                )
            except RedisError as exc:
                logger.warning(
                    f"[REDIS][{operation.upper()}][{key}] Redis error: {exc}"
                )
            return None

        return cast("F", wrapper)

    return decorator
