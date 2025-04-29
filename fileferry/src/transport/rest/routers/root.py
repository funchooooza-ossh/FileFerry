from fastapi import APIRouter

from composition.di import SystemAdapterDI
from transport.rest.dto.base import HealthCheck
from transport.rest.routers.errors import problem_router
from transport.rest.routers.files import file_router

root_router = APIRouter(prefix="/api/v1")


@root_router.get("/healthcheck", tags=["monitoring"])
async def healthcheck(adapter: SystemAdapterDI) -> HealthCheck:
    health = await adapter.healthcheck()
    data = HealthCheck.from_domain(health)
    return data


root_router.include_router(file_router)
root_router.include_router(problem_router)
