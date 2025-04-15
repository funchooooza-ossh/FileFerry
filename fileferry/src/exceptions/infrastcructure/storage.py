class StorageError(Exception):
    """
    Базовая ошибка хранилища
    """


class StorageNotFoundError(StorageError):
    """
    Файл не найден в хранилище
    """
