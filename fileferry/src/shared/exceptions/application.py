from typing import Optional

from starlette import status


class ApplicationError(Exception):
    """
    Базовый класс ошибок слоя приложения.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(
        self,
        message: str,
        *,
        type: Optional[str] = None,
        status_code: Optional[int] = None,
    ) -> None:
        super().__init__(message)
        self.type = type or self.__class__.__name__
        if status_code:
            self.status_code = status_code


class FileOperationFailed(ApplicationError):
    """
    Обертка для инфра ошибок во время обработки запроса.

    """

    pass


class InvalidFileParameters(ApplicationError):
    """
    От пользователя пришел заведомо невалидный файл.
    Пустой или с неопределяемым mime'ом или слишком длинным именем и тд.
    """

    pass


class InvalidValueError(ApplicationError):
    """
    Возникает, когда слой приложения не может преобразовать
    пользовательские данные в валидные VO.
    """

    pass


class ApplicationRunTimeError(Exception):
    """
    Исключение, сигнализирующее о нарушении инвариантов или
    неожиданных условиях в приложении.
    Используется для отладки и логирования логических ошибок.
    """

    pass


class DomainRejectedError(ApplicationError):
    """
    Обертка доменных ошибок.
    """

    pass
