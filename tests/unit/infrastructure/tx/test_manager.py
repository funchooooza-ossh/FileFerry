import pytest
from infrastructure.tx.context import SqlAlchemyTransactionContext
from infrastructure.tx.manager import TransactionManager


@pytest.mark.asyncio
@pytest.mark.unit
async def test_transaction_manager(tx_context: SqlAlchemyTransactionContext):
    manager = TransactionManager(context=tx_context)

    assert manager._started is False  # type: ignore

    await manager.start()

    assert manager._started is True  # type: ignore

    assert manager._context.session.in_transaction()  # type: ignore

    await manager.end()

    assert manager._started is False  # type: ignore

    assert not manager._context._session.in_transaction()  # type: ignore


@pytest.mark.asyncio
@pytest.mark.unit
async def test_manager_double_start_raises_error(
    tx_context: SqlAlchemyTransactionContext,
):
    manager = TransactionManager(context=tx_context)
    with pytest.raises(RuntimeError, match="Transaction has already been started"):
        await manager.start()
        await manager.start()
