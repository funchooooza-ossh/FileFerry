from contracts.application import HealthCheckUseCaseContract
from contracts.infrastructure import SQLAlchemyMinioAtomicContract
from domain.models import ComponentStatuses, HealthReport


class HealthCheckUseCase(HealthCheckUseCaseContract):
    def __init__(self, atomic: SQLAlchemyMinioAtomicContract) -> None:
        self._atomic = atomic

    async def execute(self) -> HealthReport:
        async with self._atomic as transaction:
            db_health = await transaction.data_access.healtcheck()
            storage_health = await transaction.storage.healtcheck()

            components = ComponentStatuses(db=db_health, storage=storage_health)
            return HealthReport.generate(components=components)
