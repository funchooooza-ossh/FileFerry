from collections.abc import AsyncIterator

from contracts.application import FileStorage, RetrieveFileService, UnitOfWork
from domain.models.dataclasses import FileMeta
from domain.models.value_objects import FileId
from shared.exceptions.application import FileRetrieveFailedError
from shared.exceptions.infrastructure import (
    InfrastructureError,
    InvalidBucketNameError,
    NoSuchBucketError,
    RepositoryError,
    RepositoryNotFoundError,
    RepositoryORMError,
    StorageNotFoundError,
)


class RetrieveFileServiceImpl(RetrieveFileService):
    def __init__(self, uow: UnitOfWork, storage: FileStorage) -> None:
        self._uow = uow
        self._storage = storage

    async def execute(self, file_id: FileId) -> tuple[FileMeta, AsyncIterator[bytes]]:
        try:
            async with self._uow as uow:
                meta = await uow.file_repo.get(file_id=file_id.value)
                stream = await self._storage.retrieve(file_id=file_id.value)
        except InvalidBucketNameError as exc:
            raise FileRetrieveFailedError("Имя запрошенного ресурса не валидно", type=exc.type) from exc
        except NoSuchBucketError as exc:
            raise FileRetrieveFailedError("Запрошенный ресурс не существует", type=exc.type) from exc
        except RepositoryNotFoundError as exc:
            raise FileRetrieveFailedError("Запрошенный объект не найден", type=exc.type) from exc
        except StorageNotFoundError as exc:
            raise FileRetrieveFailedError("Запрошенный объект не найден", type=exc.type) from exc
        except RepositoryORMError as exc:
            raise FileRetrieveFailedError("Ошибка обработки данных", type=exc.type) from exc
        except RepositoryError as exc:
            raise FileRetrieveFailedError("Ошибка работы с базой данных", type=exc.type) from exc
        except InfrastructureError as exc:
            raise FileRetrieveFailedError("Ошибка получения файла", type=exc.type) from exc
        else:
            return meta, stream
