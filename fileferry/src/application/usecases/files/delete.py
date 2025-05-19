from application.exceptions.infra_handler import wrap_infrastructure_failures
from contracts.application import DeleteUseCaseContract
from contracts.infrastructure import OperationCoordinationContract
from domain.models import FileId
from shared.enums import Buckets


class DeleteUseCase(DeleteUseCaseContract):
    """
    Случай использования для удаления файла из хранилища файлов и уровня доступа к данным.

    Этот класс координирует удаление файла, взаимодействуя с хранилищем файлов
    и уровнем доступа к данным через транзакционную операцию. Он гарантирует, что обе
    операции выполняются в одном транзакционном контексте для поддержания согласованности.

    Атрибуты:
        _coordinator (OperationCoordinationContract): Координатор, отвечающий за
            управление транзакционными операциями.

    Методы:
        execute(file_id: FileId, bucket: Buckets) -> None:
            Удаляет указанный файл из хранилища файлов и уровня доступа к данным
            в транзакционном контексте.
    """

    def __init__(self, coordinator: OperationCoordinationContract) -> None:
        self._coordinator = coordinator

    @wrap_infrastructure_failures
    async def execute(self, file_id: FileId, bucket: Buckets) -> None:
        async with self._coordinator as transaction:
            await transaction.data_access.delete(file_id=file_id.value)
            await transaction.file_storage.delete(file_id=file_id.value, bucket=bucket)
