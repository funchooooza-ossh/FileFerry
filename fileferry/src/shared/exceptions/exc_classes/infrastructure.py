from typing import Any


class InfraError(Exception):
    """Базовый класс для всех инфраструктурных ошибок."""

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.type = self.__class__.__name__

    pass


class DataAccessError(InfraError):
    """Ошибка, связанная с репозиторием данных (например, ошибки в SQLAlchemy)."""

    pass


class IntegrityError(DataAccessError):
    """Ошибка целостности данных (например, нарушение ограничений)."""

    pass


class OperationalError(DataAccessError):
    """Операционная ошибка при взаимодействии с базой данных."""

    pass


class ProgrammingError(DataAccessError):
    """Ошибка программирования в SQL-запросах или работе ORM."""

    pass


class NoResultFoundError(DataAccessError):
    """Ошибка, если результат не найден в базе данных (NoResultFound)."""

    pass


class MultipleResultsFoundError(DataAccessError):
    """Ошибка, если найдено несколько результатов, когда ожидался один."""

    pass


class DisconnectedError(DataAccessError):
    """Ошибка, если потеряно соединение с базой данных."""

    pass


class DatabaseError(DataAccessError):
    """Общая ошибка работы с базой данных."""

    pass


class UnknownDatabaseError(DataAccessError):
    """Неизвестная ошибка, связанная с базой данных."""

    pass


class StorageError(InfraError):
    """Ошибка взаимодействия с хранилищем (например, S3)."""

    pass


class AccessDeniedError(StorageError):
    """Ошибка доступа в S3 (Access Denied)."""

    pass


class NoSuchBucketError(StorageError):
    """Ошибка, если указанный бакет не существует."""

    pass


class NoSuchKeyError(StorageError):
    """Ошибка, если указанный ключ не найден в хранилище."""

    pass


class InvalidAccessKeyIdError(StorageError):
    """Ошибка, если неверный идентификатор ключа доступа."""

    pass


class EntityTooLargeError(StorageError):
    """Ошибка, если объект слишком большой для загрузки в S3."""

    pass


class InternalError(StorageError):
    """Внутренняя ошибка S3."""

    pass


class InvalidBucketNameError(StorageError):
    """Ошибка с неверным именем бакета в S3."""

    pass


class InvalidObjectStateError(StorageError):
    """Ошибка с неправильным состоянием объекта."""

    pass


class InvalidRangeError(StorageError):
    """Ошибка при неверном диапазоне объектов в запросе."""

    pass


class MalformedXMLStorageError(StorageError):
    """Ошибка при неправильном XML запросе."""

    pass


class MissingContentLengthError(StorageError):
    """Ошибка, если отсутствует длина содержимого в запросе."""

    pass


class PreconditionFailedError(StorageError):
    """Ошибка, если условие предварительной проверки не выполнено."""

    pass


class BucketNotEmptyError(StorageError):
    """Ошибка, если бакет не пуст."""

    pass
