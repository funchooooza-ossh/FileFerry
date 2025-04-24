import contextvars
import sys
from typing import Any

from loguru import logger as _logger

request_id_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{extra[request_id]}</cyan> | "
    "<level>{message}</level>"
)


def setup_logging() -> None:
    _logger.remove()
    _logger.add(
        sys.stdout,
        format=LOG_FORMAT,
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=False,
    )

    def add_request_id(record: dict[str, Any]) -> None:
        record["extra"]["request_id"] = request_id_ctx_var.get()

    _logger.configure(patcher=add_request_id)  # type: ignore
