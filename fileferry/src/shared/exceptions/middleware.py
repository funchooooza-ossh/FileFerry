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
            # Определяем, что предпочитает клиент в Accept заголовке
            if "application/problem+json" in request.headers.get("accept", ""):
                return JSONResponse(
                    status_code=exc.status_code if hasattr(exc, "status_code") else 400,
                    content={
                        "type": f"https://example.com/problems/{exc.type.lower()}",
                        "title": str(exc),
                        "status": (
                            exc.status_code if hasattr(exc, "status_code") else 400
                        ),
                        "detail": str(exc),
                        "instance": str(request.url.path),
                    },
                    media_type="application/problem+json",
                )
            else:
                return JSONResponse(
                    status_code=exc.status_code if hasattr(exc, "status_code") else 400,
                    content=Response.failure(msg=str(exc), type=exc.type).model_dump(),
                    media_type="application/json",
                )

        except Exception as exc:
            return JSONResponse(
                status_code=500,
                content={
                    "type": "about:blank",
                    "title": "Internal Server Error",
                    "status": 500,
                    "detail": str(exc),
                    "instance": str(request.url.path),
                },
                media_type="application/problem+json",
            )
