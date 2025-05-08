from contracts.application import (
    HealthCheckUseCaseContract,
    SnapshotUseCaseContract,
    SystemAdapterContract,
)
from infrastructure.types.health.system_health import SystemHealthReport
from infrastructure.types.task_snapshot import ManagerSnapshot
from shared.exceptions.application import ApplicationRunTimeError


class SystemAdapter(SystemAdapterContract):
    """
    Адаптер для операций, связанных с системой, реализующий интерфейс SystemAdapterContract.

    Этот класс служит мостом между уровнем приложения и вариантами использования для проверки
    состояния системы и управления снимками.

    Атрибуты:
        _health_usecase (HealthCheckUseCaseContract): Вариант использования, отвечающий за выполнение проверки состояния.
        _snapshot_usecase (SnapshotUseCaseContract): Вариант использования, отвечающий за управление снимками.

    Методы:
        healthcheck() -> SystemHealthReport:
            Выполняет проверку состояния системы с использованием предоставленного варианта использования.
            Вызывает ApplicationRunTimeError, если вариант использования проверки состояния недоступен.

        snapshot() -> ManagerSnapshot:
            Получает снимок состояния системы с использованием предоставленного варианта использования.
            Вызывает ApplicationRunTimeError, если вариант использования управления снимками недоступен.
    """

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
