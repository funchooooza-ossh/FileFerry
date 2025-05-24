import pytest
from infrastructure.tx.context import SqlAlchemyTransactionContext
from infrastructure.tx.manager import TransactionManager


@pytest.fixture(scope="function")
def tx_manager(tx_context: SqlAlchemyTransactionContext) -> TransactionManager:
    return TransactionManager(tx_context)
