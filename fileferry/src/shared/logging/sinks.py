import re
from pathlib import Path
from typing import Any, Optional

from loguru import logger as _logger

from shared.logging.formatters import LOG_FORMAT

LOG_BASE_DIR = Path("./logs")
LOGS_COMPRESSION = "gz"
SINKS_REGISTERED = {"requests", "trace"}


def create_sink(
    name: str, level: str, exclude: Optional[dict[str, str]] = None
) -> None:
    log_dir = LOG_BASE_DIR / name
    log_dir.mkdir(parents=True, exist_ok=True)

    def exclude_filter(record: dict[str, Any]) -> bool:
        if not exclude:
            return record["extra"].get("name", "") == name

        for key, value in exclude.items():
            if re.search(value, record["extra"].get(key, "")):
                return False

        return record["extra"].get("name", "") == name

    _logger.add(
        log_dir / f"{level.lower()}.log",
        level=level,
        format=LOG_FORMAT,
        enqueue=True,
        retention="1 week",
        rotation="100 MB",
        compression=LOGS_COMPRESSION,
        filter=lambda r,: exclude_filter(r),  # type: ignore
    )
