import re
import sys
from typing import Any

from loguru import logger as _logger

from shared.logging.context import get_request_id, get_scope
from shared.logging.formatters import METRICS_REGEX, STDOUT_FORMAT
from shared.logging.sinks import SINKS_REGISTERED, create_sink


def add_request_ctx(record: dict[str, Any]) -> None:
    record["extra"]["request_id"] = get_request_id()
    record["extra"]["short_request_id"] = record["extra"]["request_id"][:8]
    record["extra"]["scope"] = get_scope()
    record["extra"].setdefault("name", "default")


def setup_logging() -> None:
    _logger.remove()

    _logger.add(
        sys.stdout,
        format=STDOUT_FORMAT,
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=False,
        filter=lambda r: not re.search(METRICS_REGEX, r["extra"].get("scope", "")),
    )

    for name in SINKS_REGISTERED:
        create_sink(name, "TRACE")
        create_sink(name, "INFO", exclude={"scope": METRICS_REGEX})
        create_sink(name, "WARNING")

    _logger.configure(patcher=add_request_ctx)  # type: ignore
