LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{extra[request_id]}</cyan> | "
    "<cyan>{extra[scope]}</cyan> | "
    "<blue>{name}:{function}:{line}</blue> | "
    "<level>{message}</level>"
)

STDOUT_FORMAT = (
    "<level>{level: <8}</level> | "
    "<cyan>{extra[short_request_id]}</cyan> | "
    "<cyan>{extra[scope]}</cyan> | "
    "<level>{message}</level>"
)

METRICS_REGEX = r"GET\s+/metrics/?"
