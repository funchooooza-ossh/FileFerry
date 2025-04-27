from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.responses import Response as StarletteResponse

from shared.exceptions.exc_classes.application import ApplicationError
from transport.rest.dto.base import Response


class ApplicationErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[StarletteResponse]],
    ) -> StarletteResponse:
        try:
            response = await call_next(request)
            return response
        except ApplicationError as exc:
            return JSONResponse(
                status_code=exc.status_code if hasattr(exc, "status_code") else 400,
                content=Response.failure(msg=str(exc), type=exc.type).model_dump(),
            )
