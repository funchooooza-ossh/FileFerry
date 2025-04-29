from typing import Protocol

from domain.models import HealthReport


class SystemAdapterContract(Protocol):
    async def healthcheck(self) -> HealthReport: ...
