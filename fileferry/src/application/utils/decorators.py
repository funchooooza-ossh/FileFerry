import functools
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar, cast

from loguru import logger

from application.errors.mappers import (
    InfrastructureErrorMapper,
    map_code_to_http_status,
)
from shared.exceptions.application import FileOperationFailed
from shared.exceptions.infrastructure import InfrastructureError

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def wrap_infrastructure_failures(func: F) -> F:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)

        except InfrastructureError as exc:
            code = InfrastructureErrorMapper.get_code(exc)
            message = InfrastructureErrorMapper.get_message(exc)
            status = map_code_to_http_status(code)
            logger.warning(f"Handled infrastructure error: {exc}")
            raise FileOperationFailed(message, type=code.value, status_code=status) from exc

    return cast("F", wrapper)
