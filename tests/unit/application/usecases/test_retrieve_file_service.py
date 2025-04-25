from collections.abc import AsyncIterator
from unittest.mock import AsyncMock

import pytest
from application.errors.infra_codes import InfrastructureErrorCode
from application.errors.mappers import (
    InfrastructureErrorMapper,
    map_code_to_http_status,
)
from application.usecases.retrieve_file import RetrieveFileServiceImpl
from application.utils.decorators import wrap_infrastructure_failures
from domain.models.dataclasses import FileMeta
from domain.models.value_objects import FileId
from shared.exceptions.application import FileOperationFailed
from shared.exceptions.infrastructure import (
    InfrastructureError,
    InvalidBucketNameError,
    NoSuchBucketError,
    RepositoryError,
    RepositoryIntegrityError,
    RepositoryNotFoundError,
    RepositoryOperationalError,
    RepositoryORMError,
    RepositoryProgrammingError,
    StorageError,
    StorageNotFoundError,
)

from tests.helpers import aiter


@pytest.mark.asyncio
async def test_retrieve_success():
    file_id = FileId.new()
    file_meta = FileMeta(
        id=file_id,
        name="randname",  # type: ignore
        size=123,  # type: ignore
        content_type="application/random",  # type: ignore
    )

    file_repo = AsyncMock()
    file_repo.get.return_value = file_meta

    uow_context = AsyncMock()
    uow_context.file_repo = file_repo

    uow = AsyncMock()
    uow.__aenter__.return_value = uow_context

    storage = AsyncMock()
    storage.retrieve.return_value = aiter([b"chunk", b"chunk2"])

    usecase = RetrieveFileServiceImpl(uow=uow, storage=storage)

    meta, stream = await usecase.execute(file_id=file_id)

    assert isinstance(meta, FileMeta)
    assert isinstance(stream, AsyncIterator)
    file_repo.get.assert_awaited_once()
    storage.retrieve.assert_awaited_once()


@pytest.mark.parametrize(
    "error_cls, expected_code",
    [
        (NoSuchBucketError, InfrastructureErrorCode.NO_SUCH_BUCKET),
        (InvalidBucketNameError, InfrastructureErrorCode.INVALID_BUCKET_NAME),
        (StorageNotFoundError, InfrastructureErrorCode.STORAGE_NOT_FOUND),
        (StorageError, InfrastructureErrorCode.STORAGE),
        (RepositoryNotFoundError, InfrastructureErrorCode.REPO_NOT_FOUND),
        (RepositoryIntegrityError, InfrastructureErrorCode.REPO_INTEGRITY),
        (RepositoryOperationalError, InfrastructureErrorCode.REPO_OPERATIONAL),
        (RepositoryProgrammingError, InfrastructureErrorCode.REPO_PROGRAMMING),
        (RepositoryORMError, InfrastructureErrorCode.REPO_ORM),
        (RepositoryError, InfrastructureErrorCode.REPOSITORY),
        (InfrastructureError, InfrastructureErrorCode.INFRA),
    ],
)
@pytest.mark.asyncio
async def test_infrastructure_mapping(error_cls, expected_code):  # type: ignore
    @wrap_infrastructure_failures
    async def failing_usecase():
        raise error_cls("test")

    with pytest.raises(FileOperationFailed) as exc_info:
        await failing_usecase()

    exc = exc_info.value
    assert exc.type == expected_code.value  # type: ignore
    assert exc.status_code == map_code_to_http_status(expected_code)  # type: ignore
    assert str(exc) == InfrastructureErrorMapper.get_message(error_cls("test"))  # type: ignore
