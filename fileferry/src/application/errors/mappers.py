from starlette import status

from application.errors.infra_codes import InfrastructureErrorCode
from shared.exceptions.infrastructure import (
    InfrastructureError,
    InvalidBucketNameError,
    NoSuchBucketError,
    RepositoryError,
    RepositoryIntegrityError,
    RepositoryNotFoundError,
    RepositoryOperationalError,
    RepositoryORMError,
    RepositoryProgrammingError,
    StorageError,
    StorageNotFoundError,
)


class InfrastructureErrorMapper:
    _type_to_code: dict[type[InfrastructureError], InfrastructureErrorCode] = {
        NoSuchBucketError: InfrastructureErrorCode.NO_SUCH_BUCKET,
        InvalidBucketNameError: InfrastructureErrorCode.INVALID_BUCKET_NAME,
        StorageNotFoundError: InfrastructureErrorCode.STORAGE_NOT_FOUND,
        StorageError: InfrastructureErrorCode.STORAGE,
        RepositoryNotFoundError: InfrastructureErrorCode.REPO_NOT_FOUND,
        RepositoryIntegrityError: InfrastructureErrorCode.REPO_INTEGRITY,
        RepositoryOperationalError: InfrastructureErrorCode.REPO_OPERATIONAL,
        RepositoryProgrammingError: InfrastructureErrorCode.REPO_PROGRAMMING,
        RepositoryORMError: InfrastructureErrorCode.REPO_ORM,
        RepositoryError: InfrastructureErrorCode.REPOSITORY,
        InfrastructureError: InfrastructureErrorCode.INFRA,
    }

    _code_to_message: dict[InfrastructureErrorCode, str] = {
        InfrastructureErrorCode.NO_SUCH_BUCKET: "Указанный bucket не существует.",
        InfrastructureErrorCode.INVALID_BUCKET_NAME: "Имя bucket недопустимо.",
        InfrastructureErrorCode.STORAGE_NOT_FOUND: "Файл не найден в хранилище.",
        InfrastructureErrorCode.STORAGE: "Ошибка взаимодействия с хранилищем.",
        InfrastructureErrorCode.REPO_NOT_FOUND: "Запись не найдена в базе данных.",
        InfrastructureErrorCode.REPO_INTEGRITY: "Нарушение ограничений целостности БД.",
        InfrastructureErrorCode.REPO_OPERATIONAL: "Ошибка соединения или таймаут при работе с БД.",
        InfrastructureErrorCode.REPO_PROGRAMMING: "Ошибка в SQL или коде ORM.",
        InfrastructureErrorCode.REPO_ORM: "Ошибка ORM.",
        InfrastructureErrorCode.REPOSITORY: "Ошибка при работе с репозиторием.",
        InfrastructureErrorCode.INFRA: "Низкоуровневая инфраструктурная ошибка.",
        InfrastructureErrorCode.UNKNOWN: "Неизвестная инфраструктурная ошибка.",
    }

    @classmethod
    def get_code(cls, exc: Exception) -> InfrastructureErrorCode:
        for exc_type, code in cls._type_to_code.items():
            if isinstance(exc, exc_type):
                return code
        return InfrastructureErrorCode.UNKNOWN

    @classmethod
    def get_message(cls, exc: Exception) -> str:
        return cls._code_to_message.get(cls.get_code(exc), "Неизвестная ошибка инфраструктуры.")


def _map_code_to_http_status(code: InfrastructureErrorCode) -> int:  # noqa: C901
    match code:
        case InfrastructureErrorCode.NO_SUCH_BUCKET:
            return status.HTTP_404_NOT_FOUND
        case InfrastructureErrorCode.STORAGE_NOT_FOUND:
            return status.HTTP_404_NOT_FOUND
        case InfrastructureErrorCode.REPO_NOT_FOUND:
            return status.HTTP_404_NOT_FOUND
        case InfrastructureErrorCode.REPO_INTEGRITY:
            return status.HTTP_409_CONFLICT
        case InfrastructureErrorCode.REPO_OPERATIONAL:
            return status.HTTP_503_SERVICE_UNAVAILABLE
        case InfrastructureErrorCode.REPO_PROGRAMMING:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        case InfrastructureErrorCode.REPO_ORM:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        case InfrastructureErrorCode.REPOSITORY:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        case InfrastructureErrorCode.STORAGE:
            return status.HTTP_502_BAD_GATEWAY
        case InfrastructureErrorCode.INVALID_BUCKET_NAME:
            return status.HTTP_400_BAD_REQUEST
        case InfrastructureErrorCode.INFRA:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
        case InfrastructureErrorCode.UNKNOWN:
            return status.HTTP_500_INTERNAL_SERVER_ERROR
