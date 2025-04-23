import functools
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from loguru import logger

from application.errors.mappers import InfrastructureErrorMapper
from shared.exceptions.application import FileOperationFailed
from shared.exceptions.infrastructure import InfrastructureError

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def wrap_infrastructure_failures(func: F) -> Callable[..., Awaitable[Any]]:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)

        except InfrastructureError as exc:
            code = InfrastructureErrorMapper.get_code(exc)
            message = InfrastructureErrorMapper.get_message(exc)
            logger.warning(f"Handled infrastructure error: {exc}")
            raise FileOperationFailed(message, type=code.value) from exc

    return wrapper
