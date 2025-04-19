import pytest
from unittest.mock import AsyncMock, MagicMock
from domain.models.dataclasses import FileMeta
from infrastructure.repositories.file.sqlalchemy import FileRepository
from sqlalchemy.exc import (
    SQLAlchemyError,
    NoResultFound,
    IntegrityError,
    OperationalError,
    ProgrammingError,
)
from shared.exceptions.infrastructure import (
    RepositoryError,
    RepositoryNotFoundError,
    RepositoryIntegrityError,
    RepositoryOperationalError,
    RepositoryProgrammingError,
    RepositoryORMError,
)


@pytest.mark.asyncio
async def test_add_success(valid_filemeta, mocker):
    session = AsyncMock()
    repo = FileRepository(session)

    await repo.add(valid_filemeta)

    session.add.assert_called_once()
    session.flush.assert_called_once()


@pytest.mark.asyncio
async def test_add_invalid_filemeta_raises_error(mocker):
    session = AsyncMock()

    from_domain_mock = mocker.patch(
        "src.infrastructure.repositories.file.sqlalchemy.File.from_domain",
        side_effect=ValueError("invalid meta"),
    )

    repo = FileRepository(session)
    invalid_meta = mocker.Mock(spec=FileMeta)

    with pytest.raises(RepositoryError):
        await repo.add(invalid_meta)

    from_domain_mock.assert_called_once_with(invalid_meta)
    session.add.assert_not_called()
    session.flush.assert_not_called()


@pytest.mark.parametrize(
    "exc_type, expected_exception",
    [
        (NoResultFound, RepositoryNotFoundError),
        (IntegrityError, RepositoryIntegrityError),
        (OperationalError, RepositoryOperationalError),
        (ProgrammingError, RepositoryProgrammingError),
        (SQLAlchemyError, RepositoryORMError),
    ],
)
@pytest.mark.asyncio
async def test_add_wraps_sqlalchemy_error(valid_filemeta, exc_type, expected_exception):
    # Мокаем session
    session_mock = MagicMock()
    # Для каждого исключения передаем необходимые параметры
    if exc_type == IntegrityError:
        session_mock.add.side_effect = exc_type("mocked error", "params", "orig")
    elif exc_type == OperationalError:
        session_mock.add.side_effect = exc_type("mocked error", "params", "orig")
    elif exc_type == ProgrammingError:
        session_mock.add.side_effect = exc_type("mocked error", "params", "orig")
    else:
        session_mock.add.side_effect = exc_type("mocked error")

    session_mock.flush = AsyncMock()

    repo = FileRepository(session=session_mock)

    # Проверяем, что правильное исключение оборачивается в RepositoryError или его подкласс
    with pytest.raises(expected_exception):
        await repo.add(valid_filemeta)


@pytest.mark.parametrize(
    "exc_type, expected_exception",
    [
        (NoResultFound, RepositoryNotFoundError),
        (IntegrityError, RepositoryIntegrityError),
        (OperationalError, RepositoryOperationalError),
        (ProgrammingError, RepositoryProgrammingError),
        (SQLAlchemyError, RepositoryORMError),
    ],
)
@pytest.mark.asyncio
async def test_add_while_session_flush_wraps_sqlalchemy_error(
    valid_filemeta, exc_type, expected_exception
):
    """Аналогично проверям для session.flush()"""
    session_mock = AsyncMock()
    session_mock.add = MagicMock()

    if exc_type == IntegrityError:
        session_mock.flush.side_effect = exc_type("mocked error", "params", "orig")
    elif exc_type == OperationalError:
        session_mock.flush.side_effect = exc_type("mocked error", "params", "orig")
    elif exc_type == ProgrammingError:
        session_mock.flush.side_effect = exc_type("mocked error", "params", "orig")
    else:
        session_mock.flush.side_effect = exc_type("mocked error")

    repo = FileRepository(session=session_mock)

    with pytest.raises(expected_exception):
        await repo.add(valid_filemeta)


@pytest.mark.asyncio
async def test_get_success(valid_filemeta, valid_file):
    session_mock = AsyncMock()
    mock_query = MagicMock()
    session_mock.execute.return_value = mock_query
    mock_query.scalar_one_or_none.return_value = valid_file

    repo = FileRepository(session=session_mock)

    result = await repo.get(valid_file.id)

    assert result == valid_filemeta

    assert valid_file.to_domain() == valid_filemeta


@pytest.mark.asyncio
async def test_get_not_found():
    session_mock = AsyncMock()
    mock_query = MagicMock()
    session_mock.execute.return_value = mock_query
    mock_query.scalar_one_or_none.return_value = None

    repo = FileRepository(session=session_mock)

    with pytest.raises(RepositoryNotFoundError):
        await repo.get("some-id")
