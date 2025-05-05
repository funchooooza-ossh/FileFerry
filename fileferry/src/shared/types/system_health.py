from typing import TypedDict, cast

from shared.types.component_health import ComponentState, ComponentStatus


class SystemHealthReport(TypedDict):
    db: ComponentStatus
    storage: ComponentStatus
    cache: ComponentStatus
    overall: ComponentState


def from_components(
    dao_status: ComponentStatus,
    storage_status: ComponentStatus,
) -> SystemHealthReport:
    if dao_status.get("aggregated") is True:
        nested = dao_status.get("details", {})
        db_status = cast("ComponentStatus", nested.get("delegate", {"status": "down"}))
        cache_status = cast("ComponentStatus", nested.get("cache", {"status": "down"}))
    else:
        db_status = dao_status
        cache_status = ComponentStatus(
            status="ok", error="Cache status not included in healthcheck"
        )

    statuses = [
        db_status.get("status", "down"),
        storage_status.get("status", "down"),
        cache_status.get("status", "down"),
    ]

    if all(s == "ok" for s in statuses):
        overall = "ok"
    elif all(s == "down" for s in statuses):
        overall = "down"
    else:
        overall = "degraded"

    return {
        "db": db_status,
        "cache": cache_status,
        "storage": storage_status,
        "overall": overall,
    }
