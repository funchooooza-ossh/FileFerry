import functools
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar, cast

from loguru import logger

from shared.exceptions.exc_classes.application import FileOperationFailed
from shared.exceptions.exc_classes.infrastructure import InfraError
from shared.exceptions.mappers.infra_errors import InfraErrorMapper

logger = logger.bind(name="infra")

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def wrap_infrastructure_failures(func: F) -> F:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)

        except InfraError as exc:
            message = InfraErrorMapper.get_message(exc)
            status = InfraErrorMapper.get_http_status(exc)
            logger.warning(f"[INFRA] Handled infrastructure error: {exc}")
            raise FileOperationFailed(
                message, type=exc.type, status_code=status
            ) from exc

    return cast("F", wrapper)
