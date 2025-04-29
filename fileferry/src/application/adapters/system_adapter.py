from contracts.application import (
    HealthCheckUseCaseContract,
    SystemAdapterContract,
)
from domain.models import HealthReport
from shared.exceptions.exc_classes.application import ApplicationRunTimeError


class SystemAdapter(SystemAdapterContract):
    def __init__(self, health_usecase: HealthCheckUseCaseContract) -> None:
        self._health_usecase = health_usecase

    async def healthcheck(self) -> HealthReport:
        if not self._health_usecase:
            raise ApplicationRunTimeError("Health usecase is not available")
        return await self._health_usecase.execute()
