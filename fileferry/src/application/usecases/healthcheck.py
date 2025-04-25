from contracts.application import FileStorage, HealthCheckService, UnitOfWork
from shared.types.healthcheck import ServiceHealthStatus


class HealthCheckServiceImpl(HealthCheckService):
    def __init__(self, uow: UnitOfWork, storage: FileStorage) -> None:
        self._uow = uow
        self._storage = storage

    async def execute(self) -> ServiceHealthStatus:
        async with self._uow as uow:
            repo_status = await uow.file_repo.healthcheck()
            storage_status = await self._storage.healthcheck()

            return ServiceHealthStatus.from_infrastructure(
                repo_status=repo_status, storage_status=storage_status
            )
