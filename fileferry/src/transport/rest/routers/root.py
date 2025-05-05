from fastapi import APIRouter

from transport.rest.routers.errors import problem_router
from transport.rest.routers.files import file_router
from transport.rest.routers.system import system_router

root_router = APIRouter(prefix="/api/v1")


root_router.include_router(file_router)
root_router.include_router(problem_router)
root_router.include_router(system_router)
