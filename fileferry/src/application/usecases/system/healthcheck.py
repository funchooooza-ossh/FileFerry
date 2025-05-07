from contracts.application import HealthCheckUseCaseContract
from contracts.infrastructure import OperationCoordinationContract
from infrastructure.types.health import SystemHealthReport, from_components


class HealthCheckUseCase(HealthCheckUseCaseContract):
    def __init__(self, coordinator: OperationCoordinationContract) -> None:
        self._coordinator = coordinator

    async def execute(self) -> SystemHealthReport:
        async with self._coordinator as transaction:
            dao_health = await transaction.data_access.healthcheck()
            storage_health = await transaction.file_storage.healthcheck()

            return from_components(dao_status=dao_health, storage_status=storage_health)
