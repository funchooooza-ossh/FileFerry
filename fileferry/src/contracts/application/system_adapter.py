from typing import Protocol

from infrastructure.types.health import SystemHealthReport
from infrastructure.types.task_snapshot import ManagerSnapshot


class SystemAdapterContract(Protocol):
    async def healthcheck(self) -> SystemHealthReport: ...
    async def snapshot(self) -> ManagerSnapshot: ...
