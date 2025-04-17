class DomainError(Exception):
    """
    Базовый класс ошибок, которые возникают бизнес слое
    """

    pass


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
