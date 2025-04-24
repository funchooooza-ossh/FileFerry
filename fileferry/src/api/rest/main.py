from fastapi import FastAPI

from api.rest.routers.root import root_router
from shared.config import settings
from shared.logging.configuration import setup_logging
from shared.logging.middleware import RequestIdMiddleware

DEBUG = settings.app_debug
setup_logging()

app = FastAPI(
    title="FileFerry",
    debug=DEBUG,
    docs_url=None if not DEBUG else "/docs",
    redoc_url=None if not DEBUG else "/redoc",
    openapi_url=None if not DEBUG else "/openapi.json",
)

app.include_router(router=root_router)
app.add_middleware(RequestIdMiddleware)
