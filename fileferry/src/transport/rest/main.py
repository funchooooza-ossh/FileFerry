# type: ignore
from prometheus_client import make_asgi_app
from starlette.types import ASGIApp

from composition.create_app import create_app
from monitoring.middleware import HttpRequestLatencyMiddleware
from shared.exceptions.middleware import ApplicationErrorMiddleware
from shared.logging import LoggingMiddleware
from transport.rest.routers.root import root_router

app = create_app(
    middlewares=[
        ApplicationErrorMiddleware,
        LoggingMiddleware,
        HttpRequestLatencyMiddleware,
    ],
    routers=[root_router],
)

metrics_app: ASGIApp = make_asgi_app()
app.mount("/metrics", metrics_app)
app.mount("/metrics/", metrics_app)
