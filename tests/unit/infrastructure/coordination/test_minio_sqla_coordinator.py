from unittest.mock import AsyncMock

import pytest
from infrastructure.coordination.minio_sqla import SqlAlchemyMinioCoordinator
from infrastructure.tx.manager import TransactionManager


@pytest.mark.asyncio
@pytest.mark.unit
async def test_autocommit_on_success_with_cached(
    tx_manager: TransactionManager, mock_minio_storage: AsyncMock, cached_dao: AsyncMock
):
    tx_manager.apply = AsyncMock()
    tx_manager.reject = AsyncMock()
    tx_manager.start = AsyncMock()
    tx_manager.end = AsyncMock()

    async with SqlAlchemyMinioCoordinator(
        transaction=tx_manager,
        storage=mock_minio_storage,
        data_access=cached_dao,
    ):
        # внутри блока никаких исключений
        pass

    tx_manager.start.assert_awaited_once()
    tx_manager.apply.assert_awaited_once()
    tx_manager.reject.assert_not_called()
    tx_manager.end.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_autorollback_on_error_with_cached(
    tx_manager: TransactionManager, mock_minio_storage: AsyncMock, cached_dao: AsyncMock
):
    tx_manager.apply = AsyncMock()
    tx_manager.reject = AsyncMock()
    tx_manager.start = AsyncMock()
    tx_manager.end = AsyncMock()

    class DummyError(Exception):
        pass

    with pytest.raises(DummyError):
        async with SqlAlchemyMinioCoordinator(
            transaction=tx_manager,
            storage=mock_minio_storage,
            data_access=cached_dao,
        ):
            raise DummyError("force rollback")

    tx_manager.start.assert_awaited_once()
    tx_manager.reject.assert_awaited_once()
    tx_manager.apply.assert_not_called()
    tx_manager.end.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_exposes_storage_and_data_access_with_cached(
    tx_manager: TransactionManager, mock_minio_storage: AsyncMock, cached_dao: AsyncMock
):
    coordinator = SqlAlchemyMinioCoordinator(
        transaction=tx_manager,
        storage=mock_minio_storage,
        data_access=cached_dao,
    )

    assert coordinator.file_storage is mock_minio_storage
    assert coordinator.data_access is cached_dao


@pytest.mark.asyncio
@pytest.mark.unit
async def test_coordinator_starts_transaction_with_cached(
    tx_manager: TransactionManager, mock_minio_storage: AsyncMock, cached_dao: AsyncMock
):
    coordinator = SqlAlchemyMinioCoordinator(
        transaction=tx_manager,
        storage=mock_minio_storage,
        data_access=cached_dao,
    )

    async with coordinator as cord:
        assert cord._transaction._started  # type: ignore
        assert cord.data_access._delegate.session.in_transaction()  # type: ignore


@pytest.mark.asyncio
@pytest.mark.unit
async def test_autocommit_on_success_with_sql(
    tx_manager: TransactionManager, mock_minio_storage: AsyncMock, sql_dao: AsyncMock
):
    tx_manager.apply = AsyncMock()
    tx_manager.reject = AsyncMock()
    tx_manager.start = AsyncMock()
    tx_manager.end = AsyncMock()

    async with SqlAlchemyMinioCoordinator(
        transaction=tx_manager,
        storage=mock_minio_storage,
        data_access=sql_dao,
    ):
        pass

    tx_manager.start.assert_awaited_once()
    tx_manager.apply.assert_awaited_once()
    tx_manager.reject.assert_not_called()
    tx_manager.end.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_autorollback_on_error_with_sql(
    tx_manager: TransactionManager, mock_minio_storage: AsyncMock, sql_dao: AsyncMock
):
    tx_manager.apply = AsyncMock()
    tx_manager.reject = AsyncMock()
    tx_manager.start = AsyncMock()
    tx_manager.end = AsyncMock()

    class DummyError(Exception):
        pass

    with pytest.raises(DummyError):
        async with SqlAlchemyMinioCoordinator(
            transaction=tx_manager,
            storage=mock_minio_storage,
            data_access=sql_dao,
        ):
            raise DummyError("rollback trigger")

    tx_manager.start.assert_awaited_once()
    tx_manager.reject.assert_awaited_once()
    tx_manager.apply.assert_not_called()
    tx_manager.end.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.unit
async def test_exposes_storage_and_data_access_with_sql(
    tx_manager: TransactionManager, mock_minio_storage: AsyncMock, sql_dao: AsyncMock
):
    coordinator = SqlAlchemyMinioCoordinator(
        transaction=tx_manager,
        storage=mock_minio_storage,
        data_access=sql_dao,
    )

    assert coordinator.file_storage is mock_minio_storage
    assert coordinator.data_access is sql_dao


@pytest.mark.asyncio
@pytest.mark.unit
async def test_coordinator_starts_transaction_with_sql(
    tx_manager: TransactionManager, mock_minio_storage: AsyncMock, sql_dao: AsyncMock
):
    coordinator = SqlAlchemyMinioCoordinator(
        transaction=tx_manager,
        storage=mock_minio_storage,
        data_access=sql_dao,
    )

    async with coordinator as cord:
        assert cord._transaction._started  # type: ignore
        assert cord.data_access.session.in_transaction()  # type: ignore
