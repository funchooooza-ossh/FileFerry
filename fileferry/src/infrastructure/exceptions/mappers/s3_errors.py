from enum import StrEnum


class S3ErrorCode(StrEnum):
    AccessDenied = "AccessDenied"
    NoSuchBucket = "NoSuchBucket"
    NoSuchKey = "NoSuchKey"
    InvalidAccessKeyID = "InvalidAccessKeyId"
    EntityTooLarge = "EntityTooLarge"
    EntityTooSmall = "EntityTooSmall"
    InternalError = "InternalError"
    InvalidBucketName = "InvalidBucketName"
    InvalidObjectState = "InvalidObjectState"
    InvalidRange = "InvalidRange"
    MalformedXML = "MalformedXML"
    MissingContentLength = "MissingContentLength"
    PreconditionFailed = "PreconditionFailed"
    BucketNotEmpty = "BucketNotEmpty"
    Unknown = "Unknown"


class S3ErrorCodeMapper:
    """Маппер для строковых значений ошибок S3 в enum S3ErrorCode."""

    @classmethod
    def from_string(cls, error_str: str) -> S3ErrorCode:
        """Возвращает значение из S3ErrorCode по строковому значению."""
        try:
            # Преобразуем строку в соответствующий элемент из S3ErrorCode
            return S3ErrorCode[error_str]
        except KeyError:
            # Если значение не найдено, возвращаем S3ErrorCode.UNKNOWN
            return S3ErrorCode.Unknown
