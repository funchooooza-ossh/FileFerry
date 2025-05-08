from enum import StrEnum

from sqlalchemy.exc import DisconnectionError as SQLAlchemyDisconnectionError
from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
from sqlalchemy.exc import MultipleResultsFound as SQLAlchemyMultipleResultsFound
from sqlalchemy.exc import NoResultFound as SQLAlchemyNoResultFound
from sqlalchemy.exc import OperationalError as SQLAlchemyOperationalError
from sqlalchemy.exc import ProgrammingError as SQLAlchemyProgrammingError

from shared.exceptions.infrastructure import (
    DataAccessError,
    DisconnectedError,
    IntegrityError,
    MultipleResultsFoundError,
    NoResultFoundError,
    OperationalError,
    ProgrammingError,
    UnknownDatabaseError,
)


class SQLAlchemyErrorCode(StrEnum):
    INTEGRITY_ERROR = "IntegrityError"
    OPERATIONAL_ERROR = "OperationalError"
    PROGRAMMING_ERROR = "ProgrammingError"
    DATABASE_ERROR = "DatabaseError"
    NO_RESULT = "NoResultFound"
    MULTIPLE_RESULTS = "MultipleResultsFound"
    DISCONNECTED = "DisconnectedError"
    UNKNOWN = "Unknown"


class SQLAlchemyErrorMapper:
    """Маппер для оборачивания ошибок SQLAlchemy в ошибки приложения."""

    @classmethod
    def map_error(cls, exc: Exception) -> DataAccessError:
        """Маппит ошибки SQLAlchemy в ошибки приложения."""

        if isinstance(exc, SQLAlchemyIntegrityError):
            return IntegrityError("Database integrity constraint violation.")
        elif isinstance(exc, SQLAlchemyOperationalError):
            return OperationalError(
                "Operational error while interacting with the database."
            )
        elif isinstance(exc, SQLAlchemyProgrammingError):
            return ProgrammingError("SQL programming error or ORM issue.")
        elif isinstance(exc, SQLAlchemyNoResultFound):
            return NoResultFoundError("No result found for the query.")
        elif isinstance(exc, SQLAlchemyMultipleResultsFound):
            return MultipleResultsFoundError(
                "Multiple results found where one was expected."
            )
        elif isinstance(exc, SQLAlchemyDisconnectionError):
            return DisconnectedError("Disconnected from the database.")

        return UnknownDatabaseError(f"Unexpected database error: {exc!s}")
