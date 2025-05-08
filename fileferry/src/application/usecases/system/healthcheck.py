from contracts.application import HealthCheckUseCaseContract
from contracts.infrastructure import OperationCoordinationContract
from infrastructure.types.health import SystemHealthReport, from_components


class HealthCheckUseCase(HealthCheckUseCaseContract):
    """
    Класс для выполнения проверки состояния системы.

    Этот класс реализует контракт HealthCheckUseCaseContract и используется для
    выполнения проверки состояния различных компонентов системы, таких как
    доступ к данным и файловое хранилище.

    Атрибуты:
        _coordinator (OperationCoordinationContract): Контракт для управления
        операциями и транзакциями.

    Методы:
        execute() -> SystemHealthReport:
            Асинхронный метод для выполнения проверки состояния системы.
            Возвращает отчет о состоянии системы.
    """

    def __init__(self, coordinator: OperationCoordinationContract) -> None:
        self._coordinator = coordinator

    async def execute(self) -> SystemHealthReport:
        async with self._coordinator as transaction:
            dao_health = await transaction.data_access.healthcheck()
            storage_health = await transaction.file_storage.healthcheck()

            return from_components(dao_status=dao_health, storage_status=storage_health)
