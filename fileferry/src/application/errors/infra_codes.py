from enum import StrEnum


class InfrastructureErrorCode(StrEnum):
    NO_SUCH_BUCKET = "NoSuchBucketError"
    INVALID_BUCKET_NAME = "InvalidBucketNameError"
    STORAGE_NOT_FOUND = "StorageNotFoundError"
    STORAGE = "StorageError"

    REPO_NOT_FOUND = "RepositoryNotFoundError"
    REPO_INTEGRITY = "RepositoryIntegrityError"
    REPO_OPERATIONAL = "RepositoryOperationalError"
    REPO_PROGRAMMING = "RepositoryProgrammingError"
    REPO_ORM = "RepositoryORMError"
    REPOSITORY = "RepositoryError"

    INFRA = "InfrastructureError"
    UNKNOWN = "UnknownInfrastructureError"
