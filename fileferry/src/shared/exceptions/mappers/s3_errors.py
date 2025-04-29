from enum import StrEnum


class S3ErrorCode(StrEnum):
    ACCESS_DENIED = "AccessDenied"
    NO_SUCH_BUCKET = "NoSuchBucket"
    NO_SUCH_KEY = "NoSuchKey"
    INVALID_ACCESS_KEY_ID = "InvalidAccessKeyId"
    ENTITY_TOO_LARGE = "EntityTooLarge"
    ENTITY_TOO_SMALL = "EntityTooSmall"
    INTERNAL_ERROR = "InternalError"
    INVALID_BUCKET_NAME = "InvalidBucketName"
    INVALID_OBJECT_STATE = "InvalidObjectState"
    INVALID_RANGE = "InvalidRange"
    MALFORMED_XML = "MalformedXML"
    MISSING_CONTENT_LENGTH = "MissingContentLength"
    PRECONDITION_FAILED = "PreconditionFailed"
    BUCKET_NOT_EMPTY = "BucketNotEmpty"
    UNKNOWN = "Unknown"


class S3ErrorCodeMapper:
    """Маппер для строковых значений ошибок S3 в enum S3ErrorCode."""

    @classmethod
    def from_string(cls, error_str: str) -> S3ErrorCode:
        """Возвращает значение из S3ErrorCode по строковому значению."""
        try:
            # Преобразуем строку в соответствующий элемент из S3ErrorCode
            return S3ErrorCode[error_str.upper()]
        except KeyError:
            # Если значение не найдено, возвращаем S3ErrorCode.UNKNOWN
            return S3ErrorCode.UNKNOWN
