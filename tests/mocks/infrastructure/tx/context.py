import pytest
from infrastructure.tx.context import SqlAlchemyTransactionContext
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="function")
async def tx_context(session: AsyncSession) -> SqlAlchemyTransactionContext:
    return SqlAlchemyTransactionContext(session=session)
