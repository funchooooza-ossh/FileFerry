from unittest.mock import AsyncMock

import pytest
from infrastructure.tx.context import SqlAlchemyTransactionContext
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
@pytest.mark.unit
async def test_tx_context(session: AsyncSession):
    ctx = SqlAlchemyTransactionContext(session=session)

    await ctx.begin()

    assert ctx.session.in_transaction()
    assert ctx._transaction is not None  # type: ignore

    await ctx.close()

    assert not ctx._session.in_transaction()  # type: ignore


@pytest.mark.asyncio
@pytest.mark.unit
async def test_tx_context_raises_runtime_error(session: AsyncSession):
    ctx = SqlAlchemyTransactionContext(session=session)

    with pytest.raises(
        RuntimeError, match="Attempt to access session before transaction started"
    ):
        session = ctx.session


@pytest.mark.asyncio
@pytest.mark.unit
async def test_tx_context_usage(session: AsyncSession):
    ctx = SqlAlchemyTransactionContext(session=session)

    await ctx.begin()

    result = await ctx.session.execute(text("SELECT version()"))
    version = result.fetchone()

    assert version is not None

    await ctx.close()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_commit_does_nothing_when_transaction_is_none():
    session = AsyncMock()
    ctx = SqlAlchemyTransactionContext(session=session)

    ctx._transaction = None  # type: ignore
    await ctx.commit()

    session.commit.assert_not_called()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_rollback_does_nothing_when_transaction_is_none():
    session = AsyncMock()
    ctx = SqlAlchemyTransactionContext(session=session)

    ctx._transaction = None  # type: ignore
    await ctx.rollback()

    session.rollback.assert_not_called()
