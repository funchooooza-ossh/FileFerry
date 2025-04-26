from contracts.application import HealthCheckService
from contracts.composition import HealthCheckAPIAdapterContract
from shared.types.healthcheck import ServiceHealthStatus


class HealthCheckAPIAdapter(HealthCheckAPIAdapterContract):
    def __init__(self, health_service: HealthCheckService) -> None:
        self._healther = health_service

    async def healthcheck(self) -> ServiceHealthStatus:
        return await self._healther.execute()
