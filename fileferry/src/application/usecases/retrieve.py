from collections.abc import AsyncIterator

from contracts.application.usecases import RetrieveUseCaseContract
from contracts.infrastructure import SQLAlchemyMinioAtomicContract
from domain.models import FileId, FileMeta
from shared.enums import Buckets
from shared.exceptions.exc_classes.application import InvalidValueError
from shared.exceptions.handlers.infra_hanlder import wrap_infrastructure_failures


class RetrieveUseCase(RetrieveUseCaseContract):
    def __init__(self, atomic: SQLAlchemyMinioAtomicContract) -> None:
        self._atomic = atomic

    @wrap_infrastructure_failures
    async def execute(
        self, file_id: str, bucket: Buckets
    ) -> tuple[FileMeta, AsyncIterator[bytes]]:
        """
        UseCase получения файла из хранилища MiniO и базы данных.
        Выполняет !!!строго последовательно!!! запрос в базу и хранилище.
        Почему последовательно? Асинхронные сессии не любят параллельные операци,
        потому что в случае падения ошибки внутри DataAccess сессия останется
        в состоянии незавершенной транзакции и gracefull close нам уже не светит.
        """
        try:
            FileId(file_id)
        except ValueError as exc:
            raise InvalidValueError("Невалидный файл айди") from exc

        async with self._atomic.transactional(False) as transaction:
            meta = await transaction.data_access.get(file_id=file_id)
            stream = await transaction.storage.retrieve(file_id=file_id, bucket=bucket)

        return meta, stream
