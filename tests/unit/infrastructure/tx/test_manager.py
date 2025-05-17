from unittest.mock import AsyncMock

import pytest
from infrastructure.tx.context import SqlAlchemyTransactionContext
from infrastructure.tx.manager import TransactionManager


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.parametrize(
    "method",
    [
        ("apply"),
        ("reject"),
    ],
)
async def test_transaction_manager(
    tx_context: SqlAlchemyTransactionContext, method: str
):
    manager = TransactionManager(context=tx_context)

    assert manager._started is False  # type: ignore

    method_to_await = object.__getattribute__(manager, method)

    await manager.start()

    assert manager._started is True  # type: ignore

    assert manager._context.session.in_transaction()  # type: ignore
    await method_to_await()
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


@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.parametrize(
    ("manager_method", "context_method"),
    [
        ("end", "close"),
        ("apply", "commit"),
        ("reject", "rollback"),
    ],
)
async def test_not_started_manager_not_calling_context(
    tx_context: SqlAlchemyTransactionContext, manager_method: str, context_method: str
):
    manager = TransactionManager(context=tx_context)
    object.__setattr__(tx_context, context_method, AsyncMock())
    assertion_method = object.__getattribute__(tx_context, context_method)
    awaiting_method = object.__getattribute__(manager, manager_method)

    await awaiting_method()
    assertion_method.assert_not_awaited()
