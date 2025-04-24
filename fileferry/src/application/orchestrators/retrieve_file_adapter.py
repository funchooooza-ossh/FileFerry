from collections.abc import AsyncIterator

from contracts.application import RetrieveFileService
from contracts.composition import RetrieveAPIAdapterContract
from domain.models.dataclasses import FileMeta
from domain.models.value_objects import FileId
from shared.exceptions.application import InvalidValueError


class RetrieveFileAPIAdapter(RetrieveAPIAdapterContract):
    def __init__(
        self,
        retrieve_service: RetrieveFileService,
    ) -> None:
        self._retriever = retrieve_service

    async def get(self, file_id: str) -> tuple[FileMeta, AsyncIterator[bytes]]:
        try:
            file_id_vo = FileId(value=file_id)
        except ValueError as exc:
            raise InvalidValueError("Невалидный id файла") from exc

        return await self._retriever.execute(file_id=file_id_vo)
