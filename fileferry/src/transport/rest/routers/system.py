from fastapi import APIRouter

from composition.di import SystemAdapterDI
from monitoring.healtcheck import (
    healthcheck_latency_seconds,
    observe_health_status,
    service_uptime_seconds,
)
from monitoring.latency import record_latency
from transport.rest.dependencies.server import UptimeDI
from transport.rest.dto.base import HealthCheck

system_router = APIRouter(prefix="/system")


@system_router.get("/healthcheck", tags=["monitoring"])
@record_latency(healthcheck_latency_seconds)
async def healthcheck(adapter: SystemAdapterDI, uptime: UptimeDI) -> HealthCheck:
    health = await adapter.healthcheck()
    data = HealthCheck.from_domain(report=health, uptime=uptime)

    observe_health_status(data.components["overall"])
    service_uptime_seconds.set(float(uptime))

    return data
