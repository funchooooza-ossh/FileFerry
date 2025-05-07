from pydantic import BaseModel

from infrastructure.types.health.system_health import SystemHealthReport
from infrastructure.types.task_snapshot import ManagerSnapshot


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
