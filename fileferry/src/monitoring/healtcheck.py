from prometheus_client import Counter, Gauge, Histogram

from shared.types.component_health import ComponentState

healthcheck_latency_seconds = Histogram(
    "fileferry_healthcheck_latency", "Latency of healthcheck endpoint in seconds"
)

healthcheck_status = Gauge(
    "fileferry_status", "Overall system health status: 1 = ok, 0 = degraded, -1 = down"
)


healthcheck_ok = Counter("fileferry_ok", "Overall system is ok counter")
healthcheck_degraded = Counter(
    "fileferry_degraded", "Overall system is degraded counter"
)
healthcheck_down = Counter("fileferry_down", "Overall system is down counter")
service_uptime_seconds = Gauge("fileferry_uptime", "Service uptime in seconds")


def observe_health_status(overall: ComponentState) -> None:
    match overall:
        case "ok":
            healthcheck_status.set(1)
            healthcheck_ok.inc()
        case "degraded":
            healthcheck_status.set(0)
            healthcheck_degraded.inc()
        case "down":
            healthcheck_status.set(-1)
            healthcheck_down.inc()
