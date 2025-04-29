from fastapi import APIRouter, Request

from composition.di import SystemAdapterDI
from transport.rest.dependencies.server import UptimeDI
from transport.rest.dto.base import HealthCheck
from transport.rest.routers.errors import problem_router
from transport.rest.routers.files import file_router

root_router = APIRouter(prefix="/api/v1")


@root_router.get("/healthcheck", tags=["monitoring"])
async def healthcheck(
    request: Request, adapter: SystemAdapterDI, uptime: UptimeDI
) -> HealthCheck:
    health = await adapter.healthcheck()
    data = HealthCheck.from_domain(report=health, uptime=uptime)
    return data


root_router.include_router(file_router)
root_router.include_router(problem_router)
