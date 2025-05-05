from typing import Protocol

from shared.types.system_health import SystemHealthReport


class SystemAdapterContract(Protocol):
    async def healthcheck(self) -> SystemHealthReport: ...
