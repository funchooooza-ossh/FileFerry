from enum import StrEnum


class FileStatus(StrEnum):
    PENDING = "pending"
    STORED = "stored"
    FAILED = "failed"
