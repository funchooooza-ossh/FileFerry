from pathlib import Path

from loguru import logger as _logger

from shared.logging.formatters import LOG_FORMAT

LOG_BASE_DIR = Path("./logs")
LOGS_COMPRESSION = "gz"
SINKS_REGISTERED = {"requests", "trace"}


def create_sink(name: str, level: str) -> None:
    log_dir = LOG_BASE_DIR / name
    log_dir.mkdir(parents=True, exist_ok=True)
    _logger.add(
        log_dir / f"{level.lower()}.log",
        level=level,
        format=LOG_FORMAT,
        enqueue=True,
        retention="1 week",
        rotation="100 MB",
        compression=LOGS_COMPRESSION,
        filter=lambda r, n=name: r["extra"].get("name", "") == n,
    )
