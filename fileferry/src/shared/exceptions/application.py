from typing import Optional


class ApplicationError(Exception):
    """
    Базовый класс ошибок слоя приложения.
    """

    def __init__(
        self,
        message: str,
        *,
        type: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.type = type or self.__class__.__name__


class DomainRejectedError(ApplicationError):
    """
    Доменный слой "отказал" в исполнении логики.
    """

    pass


class StatusFailedError(ApplicationError):
    """
    Доменный слой вернул status failed
    """

    pass
