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
