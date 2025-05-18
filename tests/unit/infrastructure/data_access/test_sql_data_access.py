import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from domain.models import FileMeta
from infrastructure.data_access.alchemy import SQLAlchemyFileMetaDataAccess
from infrastructure.tx.context import SqlAlchemyTransactionContext
from shared.exceptions.infrastructure import (
    DataAccessError,
    DisconnectedError,
    MultipleResultsFoundError,
    NoResultFoundError,
)
from shared.exceptions.infrastructure import (
    IntegrityError as AppIntegrityError,
)
from shared.exceptions.infrastructure import (
    OperationalError as AppOperationalError,
)
from shared.exceptions.infrastructure import (
    ProgrammingError as AppProgrammingError,
)
from sqlalchemy.exc import (
    DisconnectionError,
    IntegrityError,
    MultipleResultsFound,
    NoResultFound,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.unit
@pytest.mark.asyncio
async def test_sql_data_access_save_get(
    tx_context: SqlAlchemyTransactionContext, filemeta: FileMeta
):
    dao = SQLAlchemyFileMetaDataAccess(context=tx_context)

    await tx_context.begin()

    await dao.save(filemeta)

    meta = await dao.get(filemeta.get_id())

    assert meta.get_id() == filemeta.get_id()
    assert meta.get_size() == filemeta.get_size()
    assert meta.get_content_type() == filemeta.get_content_type()
    assert meta.get_name() == filemeta.get_name()

    await tx_context.close()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_sql_data_access_save_delete(
    tx_context: SqlAlchemyTransactionContext, filemeta: FileMeta
):
    dao = SQLAlchemyFileMetaDataAccess(context=tx_context)

    await tx_context.begin()

    await dao.save(filemeta)

    meta = await dao.get(filemeta.get_id())

    await dao.delete(meta.get_id())

    with pytest.raises(NoResultFoundError):
        new_meta = await dao.get(meta.get_id())

        assert meta
        assert not new_meta


@pytest.mark.unit
@pytest.mark.asyncio
async def test_sql_data_access_save_update(
    tx_context: SqlAlchemyTransactionContext, filemeta: FileMeta
):
    filemeta_to_replace = FileMeta.from_raw(
        id=filemeta.get_id(),
        name="replaced_filename",
        content_type="application/pdf",
        size=55562,
    )

    dao = SQLAlchemyFileMetaDataAccess(context=tx_context)

    await tx_context.begin()

    await dao.save(filemeta)

    meta = await dao.get(filemeta.get_id())

    await dao.update(meta=filemeta_to_replace)

    replaced_meta = await dao.get(meta.get_id())
    await tx_context.close()

    assert meta.get_name() != replaced_meta.get_name()
    assert meta.get_size() != replaced_meta.get_size()
    assert meta.get_id() == replaced_meta.get_id()


@pytest.mark.unit
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "method_name, exception, expected_error, mock_method_name",
    [
        ("save", IntegrityError, AppIntegrityError, "flush"),
        ("save", OperationalError, AppOperationalError, "flush"),
        ("save", ProgrammingError, AppProgrammingError, "flush"),
        ("get", NoResultFound, NoResultFoundError, "execute"),
        ("get", MultipleResultsFound, MultipleResultsFoundError, "execute"),
        ("get", DisconnectionError, DisconnectedError, "execute"),
        ("get", DataAccessError, DataAccessError, "execute"),
        ("get", Exception, DataAccessError, "execute"),
        ("get", RuntimeError, DataAccessError, "execute"),
    ],
)
async def test_sqlalchemy_error_mapping(
    method_name: str,
    exception: type[Exception],
    expected_error: type[Exception],
    mock_method_name: str,
    mock_session: AsyncSession,
):
    _uuid = uuid.uuid4().hex
    tx_context = SqlAlchemyTransactionContext(session=mock_session)
    dao = SQLAlchemyFileMetaDataAccess(context=tx_context)

    if issubclass(exception, IntegrityError):
        exc_instance = exception("statement", {"param": "value"}, Exception("Mocked"))
    elif issubclass(exception, (OperationalError, ProgrammingError)):
        exc_instance = exception("statement", {"param": "value"}, Exception("Mocked"))
    else:
        exc_instance = exception("Mocked SQLAlchemy Error")

    mocked_method = getattr(mock_session, mock_method_name)
    mocked_method.side_effect = exc_instance

    file_meta = FileMeta.from_raw(
        id=_uuid, name="filename", content_type="application/pdf", size=123
    )

    await tx_context.begin()
    with pytest.raises(expected_error):
        if method_name == "save":
            await dao.save(file_meta)
        else:
            await dao.get(_uuid)

    mocked_method.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.parametrize(
    "latency, version, exception, expected_status, expected_version",
    [
        (0.05, "PostgreSQL 14.1", None, "ok", "PostgreSQL 14.1"),
        (0.15, "PostgreSQL 14.1", None, "degraded", "PostgreSQL 14.1"),
        (0.05, None, None, "ok", "unknown"),
        (
            0.05,
            None,
            OperationalError("statement", {"param": "value"}, Exception("Mocked")),
            "down",
            "unknown",
        ),
        (
            0.05,
            None,
            IntegrityError("statement", {"param": "value"}, Exception("Mocked")),
            "down",
            "unknown",
        ),
        (
            0.05,
            None,
            ProgrammingError("statement", {"param": "value"}, Exception("Mocked")),
            "down",
            "unknown",
        ),
    ],
)
async def test_healthcheck(
    latency: float,
    version: str,
    exception: type[Exception] | None,
    expected_status: str,
    expected_version: str,
):
    mock_session = AsyncMock()
    mock_version_result = MagicMock()
    mock_version_result.fetchone.return_value = (version,) if version else None

    if exception:
        mock_session.execute = AsyncMock(side_effect=exception)
    else:
        mock_session.execute = AsyncMock(return_value=mock_version_result)

    tx_context = SqlAlchemyTransactionContext(session=mock_session)
    dao = SQLAlchemyFileMetaDataAccess(context=tx_context)
    with patch("time.perf_counter", side_effect=[0, latency]):
        await tx_context.begin()
        result = await dao.healthcheck()
        print(result)
    assert result.get("status") == expected_status
    assert result.get("details", {}).get("version") == expected_version

    if exception:
        assert result.get("error") == str(exception)
    else:
        assert result["latency_ms"] == pytest.approx(latency * 1000, rel=0.1)  # type: ignore

    expected_calls = 1 if exception else 2
    assert mock_session.execute.call_count == expected_calls
