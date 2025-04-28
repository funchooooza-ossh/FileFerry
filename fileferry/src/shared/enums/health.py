from enum import StrEnum

from loguru import logger


class HealthStatus(StrEnum):
    OK = "ok"
    DEGRADED = "degraded"
    DOWN = "down"

    @classmethod
    def from_boolean(cls, *statuses: bool) -> "HealthStatus":
        if not statuses:
            logger.critical("[CRITICAL] No statuses. Healthcheck Error.")
            return HealthStatus.DOWN
        if all(statuses):
            return HealthStatus.OK
        if not any(statuses):
            return HealthStatus.DOWN

        return HealthStatus.DEGRADED
