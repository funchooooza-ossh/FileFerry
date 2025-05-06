import logging


class SuppressMetrics(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # Пример: suppress /metrics and /metrics/
        msg = record.getMessage()
        return "/metrics" not in msg
