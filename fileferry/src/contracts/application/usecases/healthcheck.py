from typing import Protocol

from shared.types.system_health import SystemHealthReport


class HealthCheckUseCaseContract(Protocol):
    async def execute(self) -> SystemHealthReport:
        """Возвращает статус сервиса"""
        ...
