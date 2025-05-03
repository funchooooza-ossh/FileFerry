from contracts.application import HealthCheckUseCaseContract
from contracts.infrastructure import SQLAlchemyMinioCoordinationContract
from domain.models import ComponentStatuses, HealthReport


class HealthCheckUseCase(HealthCheckUseCaseContract):
    def __init__(self, coordinator: SQLAlchemyMinioCoordinationContract) -> None:
        self._coordinator = coordinator

    async def execute(self) -> HealthReport:
        async with self._coordinator as transaction:
            db_health = await transaction.data_access.healtcheck()
            storage_health = await transaction.storage.healtcheck()

            components = ComponentStatuses(db=db_health, storage=storage_health)
            return HealthReport.generate(components=components)
