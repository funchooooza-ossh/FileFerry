from contracts.application import (
    HealthCheckUseCaseContract,
    SnapshotUseCaseContract,
    SystemAdapterContract,
)
from shared.exceptions.exc_classes.application import ApplicationRunTimeError
from shared.types.system_health import SystemHealthReport
from shared.types.task_manager import ManagerSnapshot


class SystemAdapter(SystemAdapterContract):
    def __init__(
        self,
        health_usecase: HealthCheckUseCaseContract,
        snapshot_usecase: SnapshotUseCaseContract,
    ) -> None:
        self._health_usecase = health_usecase
        self._snapshot_usecase = snapshot_usecase

    async def healthcheck(self) -> SystemHealthReport:
        if not self._health_usecase:
            raise ApplicationRunTimeError("Health usecase is not available")
        return await self._health_usecase.execute()

    async def snapshot(self) -> ManagerSnapshot:
        if not self._snapshot_usecase:
            raise ApplicationRunTimeError("Snapshot usecase is not available")
        return self._snapshot_usecase.execute()
