from typing import Any


class DomainError(Exception):
    """
    Базовый класс ошибок, которые возникают бизнес слое
    """

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.type = self.__class__.__name__


class FilePolicyViolationEror(DomainError):
    """
    Ошибка валидации.
    """

    pass


class FileUploadFailedError(DomainError):
    """
    Инфраструктурный слой отработал некорректно.
    """

    pass
