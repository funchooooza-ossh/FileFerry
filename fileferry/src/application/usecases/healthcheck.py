from contracts.application import HealthCheckUseCaseContract
from contracts.infrastructure import SQLAlchemyMinioCoordinationContract
from shared.types.system_health import SystemHealthReport, from_components


class HealthCheckUseCase(HealthCheckUseCaseContract):
    def __init__(self, coordinator: SQLAlchemyMinioCoordinationContract) -> None:
        self._coordinator = coordinator

    async def execute(self) -> SystemHealthReport:
        async with self._coordinator as transaction:
            dao_health = await transaction.db.healthcheck()
            storage_health = await transaction.storage.healthcheck()

            return from_components(dao_status=dao_health, storage_status=storage_health)
