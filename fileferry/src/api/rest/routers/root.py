from typing import TYPE_CHECKING, Optional

from fastapi import APIRouter, Query, Request

from api.rest.di_context import make_healtcheck_resolver
from api.rest.routers.files import file_router
from api.rest.schemas.models.health import HealthStatus
from contracts.composition import ScenarioName

if TYPE_CHECKING:
    from shared.types.healthcheck import ServiceHealthStatus

root_router = APIRouter(prefix="/api/v1")

root_router.include_router(router=file_router, prefix="/files")


@root_router.get("/healthcheck", tags=["healthcheck"])
async def healthcheck(
    request: Request, scenario: Optional[ScenarioName] = Query(default=None)
) -> HealthStatus:
    uptime = request.app.state.uptime
    if scenario:
        service = make_healtcheck_resolver(scenario=scenario)
        result = await service.healthcheck()
        services = {scenario: result}
        return HealthStatus.from_services(uptime=uptime, services=services)
    services: dict[ScenarioName, ServiceHealthStatus] = {}
    for s in ScenarioName:
        service = make_healtcheck_resolver(scenario=s)
        result = await service.healthcheck()
        services[s] = result

    return HealthStatus.from_services(uptime=uptime, services=services)
