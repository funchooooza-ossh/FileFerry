from fastapi import FastAPI

from api.rest.routers.root import root_router
from shared.logging.config import setup_logging
from shared.logging.middleware import RequestIdMiddleware

setup_logging()

app = FastAPI()

app.include_router(router=root_router)
app.add_middleware(RequestIdMiddleware)
