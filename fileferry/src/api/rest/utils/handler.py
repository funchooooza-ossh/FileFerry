from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, TypeVar, cast

from fastapi.responses import StreamingResponse
from loguru import logger
from pydantic import BaseModel

from api.rest.schemas.responses import Response
from shared.exceptions.application import ApplicationError

T = TypeVar("T", bound=Callable[..., Awaitable[Any]])


def api_response(expected_type: type[BaseModel] | None = None) -> Response:
    def decorator(handler: T) -> T:
        @wraps(handler)
        async def wrapper(*args: Any, **kwargs: Any) -> Response:
            try:
                result = await handler(*args, **kwargs)

                # если result — StreamingResponse, возвращаем напрямую
                if isinstance(result, StreamingResponse):
                    return result

                # если ожидается BaseModel, обернём как Response[DataT]
                if expected_type and isinstance(result, expected_type):
                    return Response.success(result)

                # иначе — возможно это уже Response[DataT]
                return result

            except ApplicationError as exc:
                logger.warning(f"Handled error in api_response: {exc}")
                return Response.failure(msg=str(exc), type=exc.type)

        return cast("T", wrapper)

    return decorator
