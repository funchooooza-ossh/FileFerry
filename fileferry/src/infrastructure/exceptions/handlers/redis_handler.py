import functools
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar, cast

from loguru import logger
from redis.exceptions import ConnectionError, RedisError, TimeoutError

logger = logger.bind(name="trace")


F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def wrap_redis_failure(operation: str, raising: bool = False) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = args[1] if len(args) > 1 else "<unknown>"
            logger.trace(f"[REDIS] → {func.__qualname__}()")
            try:
                result = await func(*args, **kwargs)
                logger.info(f"[REDIS][OK] ← {func.__qualname__}() completed")
                return result
            except (ConnectionError, TimeoutError) as exc:
                logger.warning(
                    f"[REDIS][ERR][{operation.upper()}][{key}] Connection error: {exc}"
                )
                if raising:
                    raise exc
            except RedisError as exc:
                logger.warning(
                    f"[REDIS][ERR][{operation.upper()}][{key}] Redis error: {exc}"
                )
                if raising:
                    raise exc
            return None

        return cast("F", wrapper)

    return decorator
