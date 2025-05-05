from sqlalchemy.ext.asyncio import AsyncSession

from contracts.infrastructure import TransactionContext
from infrastructure.transactions.context import SqlAlchemyTransactionContext
from infrastructure.transactions.manager import TransactionManager


def create_transaction_context(
    session_factory: AsyncSession,
) -> SqlAlchemyTransactionContext:
    return SqlAlchemyTransactionContext(session=session_factory)


def create_transaction_manager(context: TransactionContext) -> TransactionManager:
    return TransactionManager(context=context)
