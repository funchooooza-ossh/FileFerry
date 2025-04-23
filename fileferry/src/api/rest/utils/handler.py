from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any, TypeVar, cast

from fastapi.responses import JSONResponse, StreamingResponse
from loguru import logger
from pydantic import BaseModel

from api.rest.schemas.responses import Response
from shared.exceptions.application import ApplicationError

T = TypeVar("T", bound=Callable[..., Awaitable[Any]])


def api_response(expected_type: type[BaseModel] | None = None) -> Callable[[T], T]:
    def decorator(handler: T) -> T:
        @wraps(handler)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = await handler(*args, **kwargs)

                if isinstance(result, StreamingResponse):
                    return result

                if expected_type and isinstance(result, expected_type):
                    return JSONResponse(
                        status_code=200,
                        content=Response.success(result).model_dump(),
                    )

                return result

            except ApplicationError as exc:
                logger.warning(f"Handled error in api_response: {exc}")
                return JSONResponse(
                    status_code=exc.status_code if hasattr(exc, "status_code") else 400,
                    content=Response.failure(msg=str(exc), type=exc.type).model_dump(),
                )

        return cast("T", wrapper)

    return decorator
