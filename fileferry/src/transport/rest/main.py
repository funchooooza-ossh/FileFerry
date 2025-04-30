from composition.create_app import create_app
from shared.exceptions.middleware import ApplicationErrorMiddleware
from shared.logging.middleware import RequestIdMiddleware
from transport.rest.routers.root import root_router

app = create_app(
    middlewares=[ApplicationErrorMiddleware, RequestIdMiddleware], routers=[root_router]
)
