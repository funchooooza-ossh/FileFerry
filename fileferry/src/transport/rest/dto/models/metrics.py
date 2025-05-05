from pydantic import BaseModel

from shared.types.system_health import SystemHealthReport
from shared.types.task_manager import ManagerSnapshot


class HealthCheck(BaseModel):
    uptime: int
    components: SystemHealthReport

    @classmethod
    def from_domain(cls, uptime: int, report: SystemHealthReport) -> "HealthCheck":
        return HealthCheck(uptime=uptime, components=report)


class SnapshotResponse(BaseModel):
    detail: ManagerSnapshot

    @classmethod
    def from_domain(cls, snapshot: ManagerSnapshot) -> "SnapshotResponse":
        return SnapshotResponse(detail=snapshot)
