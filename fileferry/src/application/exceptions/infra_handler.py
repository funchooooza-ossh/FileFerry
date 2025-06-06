import functools
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar, cast

from loguru import logger

from infrastructure.exceptions.mappers.infra_errors import InfraErrorMapper
from shared.exceptions.application import FileOperationFailed
from shared.exceptions.infrastructure import InfraError

logger = logger.bind(name="trace")

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def wrap_infrastructure_failures(func: F) -> F:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.trace(f"[INFRA] → {func.__qualname__}()")
        try:
            result = await func(*args, **kwargs)
            logger.info(f"[INFRA][OK] ← {func.__qualname__}() completed")
            return result
        except InfraError as exc:
            message = InfraErrorMapper.get_message(exc)
            status = InfraErrorMapper.get_http_status(exc)
            logger.warning(f"[INFRA][ERR] Handled infrastructure error: {exc}")
            raise FileOperationFailed(
                message, type=exc.type, status_code=status
            ) from exc

    return cast("F", wrapper)
