class ApplicationError(Exception):
    """
    Базовый класс ошибок слоя приложения.
    """

    pass


class DomainRejectedError(Exception):
    """
    Доменный слой "отказал" в исполнении логики.
    """

    pass


class StatusFailedError(Exception):
    """
    Доменный слой вернул status Failed
    """

    def __init__(self, type: str, *args):
        super().__init__(*args)
        self.type = type
