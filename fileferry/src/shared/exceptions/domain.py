from typing import Any


class DomainError(Exception):
    """
    Базовый класс ошибок, которые возникают бизнес слое
    """

    def __init__(self, *args: Any) -> None:
        super().__init__(*args)
        self.type = self.__class__.__name__


class FilePolicyViolationError(DomainError):
    """
    Ошибка валидации.
    """

    pass
