import time
from collections.abc import Awaitable, Callable

from prometheus_client import Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

fileferry_request_latency_seconds = Histogram(
    "fileferry_request_latency_seconds",
    "Latency of HTTP requests in seconds",
    ["method", "path", "status"],
)
fileferry_request_count = Counter(
    "fileferry_request_count",
    "Count of HTTP requests in seconds",
    ["method", "path", "status"],
)


class HttpRequestLatencyMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start = time.perf_counter()
        response: Response = await call_next(request)
        elapsed = time.perf_counter() - start

        method = request.method
        status = str(response.status_code)

        route = request.scope.get("route")
        path = route.path if route else request.url.path

        fileferry_request_latency_seconds.labels(
            method=method, path=path, status=status
        ).observe(elapsed)
        fileferry_request_count.labels(method=method, path=path, status=status).inc()
        return response
