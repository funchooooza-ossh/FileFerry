from typing import Protocol

from domain.models import HealthReport


class HealthCheckUseCaseContract(Protocol):
    async def execute(self) -> HealthReport:
        """Возвращает статус сервиса"""
        ...
