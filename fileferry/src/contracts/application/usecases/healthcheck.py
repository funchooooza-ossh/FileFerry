from typing import Protocol

from infrastructure.types.health.system_health import SystemHealthReport


class HealthCheckUseCaseContract(Protocol):
    async def execute(self) -> SystemHealthReport:
        """Возвращает статус сервиса"""
        ...
