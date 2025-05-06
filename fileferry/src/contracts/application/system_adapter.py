from typing import Protocol

from shared.types.system_health import SystemHealthReport
from shared.types.task_manager import ManagerSnapshot


class SystemAdapterContract(Protocol):
    async def healthcheck(self) -> SystemHealthReport: ...
    async def snapshot(self) -> ManagerSnapshot: ...
