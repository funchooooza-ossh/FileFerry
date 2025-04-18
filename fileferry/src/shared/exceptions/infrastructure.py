from typing import Any


class InfrastructureError(Exception):
    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.type = self.__class__.__name__


class StorageError(InfrastructureError):
    """
    Базовый класс для ошибок при работе с хранилищем.
    """

    pass


class StorageNotFoundError(StorageError):
    pass


class RepositoryError(InfrastructureError):
    """
    Базовый класс для ошибок, при работе с паттерном репозиторий.
    """

    pass


class RepositoryIntegrityError(RepositoryError):
    """
    Ошибка, возникает при попытке нарушения целостности состояния базы данных.
    """

    pass


class RepositoryNotFoundError(RepositoryError):
    """

    Ошибка, возникает когда запрашиваемая запись не найдена
    """

    pass


class RepositoryORMError(RepositoryError):
    """
    Ошибка, возникает при работе с ORM
    """

    pass


class RepositoryOperationalError(RepositoryORMError):
    """
    Ошибка, возникает при ошибках во время операций. Сбой соединения с базой данных, таймаут и т.д.
    """

    pass


class RepositoryProgrammingError(RepositoryORMError):
    """
    Ошибка, возникает при ошибке в коде
    """

    pass
