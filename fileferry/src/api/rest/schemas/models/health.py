from collections.abc import Mapping
from datetime import datetime
from typing import Any

from pydantic import BaseModel, field_serializer

from contracts.composition import ScenarioName
from shared.types.healthcheck import ServiceHealthStatus


class HealthStatus(BaseModel):
    uptime: datetime
    status: bool
    detail: dict[ScenarioName, Any]

    @field_serializer("uptime")
    def serialize_uptime(self, dt: datetime) -> str:
        return dt.isoformat()

    @classmethod
    def from_services(
        cls, uptime: datetime, services: Mapping[ScenarioName, ServiceHealthStatus]
    ) -> "HealthStatus":
        overall_status = all(status.ok for status in services.values())
        details = {name: status.details for name, status in services.items()}
        return cls(uptime=uptime, status=overall_status, detail=details)
