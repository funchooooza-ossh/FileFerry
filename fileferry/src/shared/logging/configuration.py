import contextvars
import re
import sys
from pathlib import Path
from typing import Any

from loguru import logger as _logger

request_id_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)
scope_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "scope", default="unknown"
)

LOG_BASE_DIR = Path("./logs")
SINKS_REGISTERED: set[str] = {"requests", "db", "cache", "storage", "infra"}
LOGS_COMPRESSION = "gz"

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{extra[request_id]}</cyan> | "
    "<cyan>{extra[scope]}</cyan> | "
    "<blue>{name}:{function}:{line}</blue> | "
    "<level>{message}</level>"
)

METRICS_REGEX = r"GET\s+/metrics/?"


def setup_logging() -> None:
    _logger.remove()

    _logger.add(
        sys.stdout,
        format=LOG_FORMAT,
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=False,
        filter=lambda r: not re.search(METRICS_REGEX, r["extra"].get("scope", "")),
    )

    for name in SINKS_REGISTERED:
        log_dir = LOG_BASE_DIR / name
        log_dir.mkdir(parents=True, exist_ok=True)

        _logger.add(
            log_dir / "info.log",
            level="INFO",
            filter=lambda r, n=name: (
                r["extra"].get("name") == n
                and r["level"].name == "INFO"
                and not re.search(METRICS_REGEX, r["extra"].get("scope", ""))
            ),
            format=LOG_FORMAT,
            enqueue=True,
            retention="1 week",
            rotation="100 MB",
            compression=LOGS_COMPRESSION,
        )

        _logger.add(
            log_dir / "err.log",
            level="WARNING",
            filter=lambda r, n=name: r["extra"].get("name") == n
            and r["level"].no >= 30
            and not re.search(METRICS_REGEX, r["extra"].get("scope", "")),
            format=LOG_FORMAT,
            enqueue=True,
            retention="1 week",
            rotation="100 MB",
            compression=LOGS_COMPRESSION,
        )

    def add_request_ctx(record: dict[str, Any]) -> None:
        record["extra"]["request_id"] = request_id_ctx_var.get()
        record["extra"]["scope"] = scope_ctx_var.get()
        record["extra"].setdefault("name", "default")

    _logger.configure(patcher=add_request_ctx)  # type: ignore
