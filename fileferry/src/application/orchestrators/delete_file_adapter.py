from contracts.application import DeleteFileService
from contracts.composition import DeleteAPIAdapterContract
from domain.models.value_objects import FileId
from shared.exceptions.application import InvalidValueError


class DeleteFileAPIAdapter(DeleteAPIAdapterContract):
    def __init__(self, delete_service: DeleteFileService) -> None:
        self._deleter = delete_service

    async def delete(self, file_id: str) -> None:
        try:
            file_id_vo = FileId(value=file_id)
        except ValueError as exc:
            raise InvalidValueError("Невалидный id файла") from exc

        return await self._deleter.execute(file_id=file_id_vo)
