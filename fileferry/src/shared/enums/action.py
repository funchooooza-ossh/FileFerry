from enum import StrEnum


class Action(StrEnum):
    """Перечисление поддерживаемых действий для ApplicationAdapter."""

    UPLOAD = "upload"
    RETRIEVE = "retrieve"
    DELETE = "delete"
    UPDATE = "update"
    HEALTH = "healthcheck"
