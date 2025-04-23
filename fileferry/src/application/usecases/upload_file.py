from collections.abc import AsyncIterator

from contracts.application import FilePolicy, FileStorage, UnitOfWork, UploadFileService
from domain.models.dataclasses import FileMeta
from shared.exceptions.application import FileUploadFailedError
from shared.exceptions.infrastructure import (
    InfrastructureError,
    InvalidBucketNameError,
    NoSuchBucketError,
    RepositoryError,
    RepositoryORMError,
    StorageError,
)


class UploadFileServiceImpl(UploadFileService):
    def __init__(self, uow: UnitOfWork, file_policy: FilePolicy, storage: FileStorage) -> None:
        self._uow = uow
        self._policy = file_policy
        self._storage = storage

    async def execute(self, meta: FileMeta, data: AsyncIterator[bytes]) -> FileMeta:
        self._policy.is_allowed(meta.content_type, meta.size)
        try:
            async with self._uow as uow:
                await uow.file_repo.add(meta)
                await uow.commit()
                await self._storage.store(
                    stream=data,
                    file_id=meta.id.value,
                    length=meta.size.value,
                    content_type=meta.content_type.value,
                )
        except InvalidBucketNameError as exc:
            raise FileUploadFailedError("Имя запрошенного ресурса не валидно", type=exc.type) from exc
        except NoSuchBucketError as exc:
            raise FileUploadFailedError("Запрошенный ресурс не существует", type=exc.type) from exc
        except StorageError as exc:
            raise FileUploadFailedError("Внутренняя ошибка загрузки файла", type=exc.type) from exc
        except RepositoryORMError as exc:
            raise FileUploadFailedError("Ошибка обработки данных", type=exc.type) from exc
        except RepositoryError as exc:
            raise FileUploadFailedError("Ошибка работы с базой данных", type=exc.type) from exc
        except InfrastructureError as exc:
            raise FileUploadFailedError("Не удалось загрузить файл", type=exc.type) from exc
        else:
            return meta
