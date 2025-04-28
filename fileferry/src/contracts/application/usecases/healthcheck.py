from typing import Protocol

from domain.models import HealthReport


class HealthCheckUseCaseContract(Protocol):
    # TODO return type
    async def execute(self) -> HealthReport:
        """Возвращает статус сервиса"""
        ...
