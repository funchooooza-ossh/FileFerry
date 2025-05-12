from fastapi import status  # импортируем статус-коды Starlette

from infrastructure.exceptions.mappers.alchemy_errors import SQLAlchemyErrorCode
from infrastructure.exceptions.mappers.s3_errors import S3ErrorCode
from shared.exceptions.infrastructure import (
    AccessDeniedError,
    BucketNotEmptyError,
    DataAccessError,
    DisconnectedError,
    EntityTooLargeError,
    IntegrityError,
    InternalError,
    InvalidAccessKeyIdError,
    InvalidBucketNameError,
    InvalidObjectStateError,
    InvalidRangeError,
    MalformedXMLStorageError,
    MissingContentLengthError,
    MultipleResultsFoundError,
    NoResultFoundError,
    NoSuchBucketError,
    NoSuchKeyError,
    OperationalError,
    PreconditionFailedError,
    ProgrammingError,
    StorageError,
)


class InfraErrorMapper:
    """Маппер для инфраструктурных ошибок."""

    _type_to_code: dict[
        type[StorageError | DataAccessError], S3ErrorCode | SQLAlchemyErrorCode
    ] = {
        AccessDeniedError: S3ErrorCode.AccessDenied,
        NoSuchBucketError: S3ErrorCode.NoSuchBucket,
        NoSuchKeyError: S3ErrorCode.NoSuchKey,
        InvalidAccessKeyIdError: S3ErrorCode.InvalidAccessKeyID,
        EntityTooLargeError: S3ErrorCode.EntityTooLarge,
        InternalError: S3ErrorCode.InternalError,
        InvalidBucketNameError: S3ErrorCode.InvalidBucketName,
        InvalidObjectStateError: S3ErrorCode.InvalidObjectState,
        InvalidRangeError: S3ErrorCode.InvalidRange,
        MalformedXMLStorageError: S3ErrorCode.MalformedXML,
        MissingContentLengthError: S3ErrorCode.MissingContentLength,
        PreconditionFailedError: S3ErrorCode.PreconditionFailed,
        BucketNotEmptyError: S3ErrorCode.BucketNotEmpty,
        #       #       #       #       #       #       #       #
        IntegrityError: SQLAlchemyErrorCode.INTEGRITY_ERROR,
        OperationalError: SQLAlchemyErrorCode.OPERATIONAL_ERROR,
        ProgrammingError: SQLAlchemyErrorCode.PROGRAMMING_ERROR,
        NoResultFoundError: SQLAlchemyErrorCode.NO_RESULT,
        MultipleResultsFoundError: SQLAlchemyErrorCode.MULTIPLE_RESULTS,
        DisconnectedError: SQLAlchemyErrorCode.DISCONNECTED,
    }

    _str_type_to_code: dict[str, S3ErrorCode | SQLAlchemyErrorCode] = {
        "AccessDeniedError": S3ErrorCode.AccessDenied,
        "NoSuchBucketError": S3ErrorCode.NoSuchBucket,
        "NoSuchKeyError": S3ErrorCode.NoSuchKey,
        "InvalidAccessKeyIdError": S3ErrorCode.InvalidAccessKeyID,
        "EntityTooLargeError": S3ErrorCode.EntityTooLarge,
        "InternalError": S3ErrorCode.InternalError,
        "InvalidBucketNameError": S3ErrorCode.InvalidBucketName,
        "InvalidObjectStateError": S3ErrorCode.InvalidObjectState,
        "InvalidRangeError": S3ErrorCode.InvalidRange,
        "MalformedXMLStorageError": S3ErrorCode.MalformedXML,
        "MissingContentLengthError": S3ErrorCode.MissingContentLength,
        "PreconditionFailedError": S3ErrorCode.PreconditionFailed,
        "BucketNotEmptyError": S3ErrorCode.BucketNotEmpty,
        #       #       #       #       #       #       #       #
        "IntegrityError": SQLAlchemyErrorCode.INTEGRITY_ERROR,
        "OperationalError": SQLAlchemyErrorCode.OPERATIONAL_ERROR,
        "ProgrammingError": SQLAlchemyErrorCode.PROGRAMMING_ERROR,
        "NoResultFoundError": SQLAlchemyErrorCode.NO_RESULT,
        "MultipleResultsFoundError": SQLAlchemyErrorCode.MULTIPLE_RESULTS,
        "DisconnectedError": SQLAlchemyErrorCode.DISCONNECTED,
    }
    _code_to_type: dict[
        S3ErrorCode | SQLAlchemyErrorCode, type[StorageError | DataAccessError]
    ] = {
        S3ErrorCode.AccessDenied: AccessDeniedError,
        S3ErrorCode.NoSuchBucket: NoSuchBucketError,
        S3ErrorCode.NoSuchKey: NoSuchKeyError,
        S3ErrorCode.InvalidAccessKeyID: InvalidAccessKeyIdError,
        S3ErrorCode.EntityTooLarge: EntityTooLargeError,
        S3ErrorCode.InternalError: InternalError,
        S3ErrorCode.InvalidBucketName: InvalidBucketNameError,
        S3ErrorCode.InvalidObjectState: InvalidObjectStateError,
        S3ErrorCode.InvalidRange: InvalidRangeError,
        S3ErrorCode.MalformedXML: MalformedXMLStorageError,
        S3ErrorCode.MissingContentLength: MissingContentLengthError,
        S3ErrorCode.PreconditionFailed: PreconditionFailedError,
        S3ErrorCode.BucketNotEmpty: BucketNotEmptyError,
        #       #       #       #       #       #       #       #
        SQLAlchemyErrorCode.INTEGRITY_ERROR: IntegrityError,
        SQLAlchemyErrorCode.OPERATIONAL_ERROR: OperationalError,
        SQLAlchemyErrorCode.PROGRAMMING_ERROR: ProgrammingError,
        SQLAlchemyErrorCode.NO_RESULT: NoResultFoundError,
        SQLAlchemyErrorCode.MULTIPLE_RESULTS: MultipleResultsFoundError,
        SQLAlchemyErrorCode.DISCONNECTED: DisconnectedError,
    }

    _code_to_message: dict[S3ErrorCode | SQLAlchemyErrorCode, str] = {
        S3ErrorCode.AccessDenied: "Доступ к ресурсу был запрещен.",
        S3ErrorCode.NoSuchBucket: "Указанный бакет не существует.",
        S3ErrorCode.NoSuchKey: "Указанный объект не найден в хранилище.",
        S3ErrorCode.InvalidAccessKeyID: "Неверный идентификатор ключа доступа.",
        S3ErrorCode.EntityTooLarge: "Объект слишком большой для загрузки.",
        S3ErrorCode.InternalError: "Внутренняя ошибка хранилища.",
        S3ErrorCode.InvalidBucketName: "Неверное имя бакета.",
        S3ErrorCode.InvalidObjectState: "Неверное состояние объекта.",
        S3ErrorCode.InvalidRange: "Неверный диапазон для объекта.",
        S3ErrorCode.MalformedXML: "Неправильный формат XML.",
        S3ErrorCode.MissingContentLength: "Отсутствует длина содержимого.",
        S3ErrorCode.PreconditionFailed: "Не выполнено условие предварительной проверки.",
        S3ErrorCode.BucketNotEmpty: "Бакет не пуст, невозможно выполнить операцию.",
        #       #       #       #       #       #       #       #       #       #       #
        SQLAlchemyErrorCode.INTEGRITY_ERROR: "Ошибка целостности данных в базе.",
        SQLAlchemyErrorCode.OPERATIONAL_ERROR: "Операционная ошибка при взаимодействии с базой данных.",
        SQLAlchemyErrorCode.PROGRAMMING_ERROR: "Ошибка в SQL-запросе или работе ORM.",
        SQLAlchemyErrorCode.NO_RESULT: "Результат не найден в базе данных.",
        SQLAlchemyErrorCode.MULTIPLE_RESULTS: "Найдено несколько результатов, ожидался один.",
        SQLAlchemyErrorCode.DISCONNECTED: "Потеряно соединение с базой данных.",
        SQLAlchemyErrorCode.UNKNOWN: "Неизвестная ошибка базы данных.",
    }

    # Новый маппинг ошибок на статус-коды Starlette
    _code_to_http_status: dict[S3ErrorCode | SQLAlchemyErrorCode, int] = {
        S3ErrorCode.AccessDenied: status.HTTP_403_FORBIDDEN,  # 403 для AccessDenied
        S3ErrorCode.NoSuchBucket: status.HTTP_404_NOT_FOUND,  # 404 для NoSuchBucket
        S3ErrorCode.NoSuchKey: status.HTTP_404_NOT_FOUND,  # 404 для NoSuchKey
        S3ErrorCode.InvalidAccessKeyID: status.HTTP_400_BAD_REQUEST,  # 400 для InvalidAccessKeyId
        S3ErrorCode.EntityTooLarge: status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,  # 413 для EntityTooLarge
        S3ErrorCode.InternalError: status.HTTP_500_INTERNAL_SERVER_ERROR,  # 500 для InternalError
        S3ErrorCode.InvalidBucketName: status.HTTP_400_BAD_REQUEST,  # 400 для InvalidBucketName
        S3ErrorCode.InvalidObjectState: status.HTTP_400_BAD_REQUEST,  # 400 для InvalidObjectState
        S3ErrorCode.InvalidRange: status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE,  # 416 для InvalidRange
        S3ErrorCode.MalformedXML: status.HTTP_400_BAD_REQUEST,  # 400 для MalformedXML
        S3ErrorCode.MissingContentLength: status.HTTP_400_BAD_REQUEST,  # 400 для MissingContentLength
        S3ErrorCode.PreconditionFailed: status.HTTP_412_PRECONDITION_FAILED,  # 412 для PreconditionFailed
        S3ErrorCode.BucketNotEmpty: status.HTTP_409_CONFLICT,  # 409 для BucketNotEmpty
        #       #       #       #       #       #       #       #       #       #       #       #       #
        SQLAlchemyErrorCode.INTEGRITY_ERROR: status.HTTP_409_CONFLICT,  # 409 для IntegrityError
        SQLAlchemyErrorCode.OPERATIONAL_ERROR: status.HTTP_503_SERVICE_UNAVAILABLE,  # 503 для OperationalError
        SQLAlchemyErrorCode.PROGRAMMING_ERROR: status.HTTP_400_BAD_REQUEST,  # 400 для ProgrammingError
        SQLAlchemyErrorCode.NO_RESULT: status.HTTP_404_NOT_FOUND,  # 404 для NoResultFound
        SQLAlchemyErrorCode.MULTIPLE_RESULTS: status.HTTP_400_BAD_REQUEST,  # 400 для MultipleResultsFound
        SQLAlchemyErrorCode.DISCONNECTED: status.HTTP_500_INTERNAL_SERVER_ERROR,  # 500 для DisconnectedError
        SQLAlchemyErrorCode.UNKNOWN: status.HTTP_500_INTERNAL_SERVER_ERROR,  # 500 для Unknown
    }

    @classmethod
    def get_code(cls, exc: Exception) -> S3ErrorCode | SQLAlchemyErrorCode:
        """Возвращает код ошибки S3ErrorCode по типу ошибки."""
        for exc_type, code in cls._type_to_code.items():
            if isinstance(exc, exc_type):
                return code
        return S3ErrorCode.Unknown

    @classmethod
    def get_message(cls, exc: Exception) -> str:
        """Возвращает сообщение ошибки по коду ошибки."""
        return cls._code_to_message.get(
            cls.get_code(exc), "Неизвестная ошибка хранилища."
        )

    @classmethod
    def get_http_status(cls, exc: Exception) -> int:
        """Возвращает статус HTTP для данной ошибки."""
        return cls._code_to_http_status.get(
            cls.get_code(exc), status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    @classmethod
    def map_to_rfc7807(cls, exc: Exception) -> dict[str, str | int | None]:
        """Маппит ошибку в формат RFC7807."""
        code = cls.get_code(exc)
        message = cls.get_message(exc)
        status_code = cls.get_http_status(exc)

        return {
            "type": f"https://example.com/problems/{code.value.lower()}",
            "title": message,
            "status": status_code,
            "detail": message,
            "instance": None,  # Примерно указываем путь запроса, если нужно
        }

    @classmethod
    def map_str_to_rfc7807(cls, exc: str) -> dict[str, str | int | None]:
        code = cls._str_type_to_code.get(exc, S3ErrorCode.Unknown)
        message = cls._code_to_message.get(code)
        status_code = cls._code_to_http_status.get(code)

        return {
            "type": f"https://example.com/problems/{code.value.lower()}",
            "title": message,
            "status": status_code,
            "detail": message,
            "instance": None,
        }

    @classmethod
    def map_code_to_error(
        cls, error_code: S3ErrorCode | SQLAlchemyErrorCode
    ) -> type[StorageError | DataAccessError]:
        """Возвращает тип ошибки по коду ошибки S3ErrorCode."""
        return cls._code_to_type.get(error_code, StorageError)

    @classmethod
    def get_code_to_message(cls) -> dict[S3ErrorCode | SQLAlchemyErrorCode, str]:
        return cls._code_to_message

    @classmethod
    def get_code_to_http_status(cls) -> dict[S3ErrorCode | SQLAlchemyErrorCode, int]:
        return cls._code_to_http_status

    @classmethod
    def get_type_to_code(
        cls,
    ) -> dict[type[StorageError | DataAccessError], S3ErrorCode | SQLAlchemyErrorCode]:
        return cls._type_to_code

    @classmethod
    def get_str_type_to_code(cls) -> dict[str, S3ErrorCode | SQLAlchemyErrorCode]:
        return cls._str_type_to_code
