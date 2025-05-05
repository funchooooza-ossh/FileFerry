import time
from collections.abc import Sequence

from fastapi import APIRouter, FastAPI

from composition.containers.registry import get_container
from shared.config import settings
from shared.logging.configuration import setup_logging


def create_app(
    *,
    routers: Sequence[APIRouter],
    middlewares: Sequence[type],
) -> FastAPI:
    setup_logging()
    container = get_container(settings.configuration)(
        config={"with_cache": settings.cache_enabled}
    )
    app = FastAPI(
        debug=settings.app_debug,
        title="FileFerry Service",
        docs_url="/docs" if settings.app_debug else None,
        redoc_url="/redoc" if settings.app_debug else None,
        openapi_url="/openapi.json" if settings.app_debug else None,
    )
    app.state.container = container
    app.state.startup_time = time.time()
    for mw in middlewares:
        app.add_middleware(mw)

    for router in routers:
        app.include_router(router)

    container.wire(modules=["composition.di"])
    return app
