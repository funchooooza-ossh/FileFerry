from enum import StrEnum

from shared.exceptions.infrastructure import (
    InfrastructureError,
    InvalidBucketNameError,
    NoSuchBucketError,
    StorageError,
    StorageNotFoundError,
)


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


CODE_TO_ERROR_MAPPING: dict[S3ErrorCode, type[InfrastructureError]] = {
    S3ErrorCode.INTERNAL_ERROR: StorageError,
    S3ErrorCode.NO_SUCH_KEY: StorageNotFoundError,
    S3ErrorCode.NO_SUCH_BUCKET: NoSuchBucketError,
    S3ErrorCode.INVALID_BUCKET_NAME: InvalidBucketNameError,
}
