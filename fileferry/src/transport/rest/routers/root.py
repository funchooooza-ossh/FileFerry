from fastapi import APIRouter

from composition.di import AdapterDI
from transport.rest.dto.base import HealthCheck
from transport.rest.routers.files import file_router
from transport.rest.routers.problems import problem_router

root_router = APIRouter(prefix="/api/v1")


@root_router.get("/healthcheck", tags=["monitoring"])
async def healthcheck(adapter: AdapterDI) -> HealthCheck:
    health = await adapter.healthcheck()
    data = HealthCheck.from_domain(health)
    return data


root_router.include_router(file_router)
root_router.include_router(problem_router)
