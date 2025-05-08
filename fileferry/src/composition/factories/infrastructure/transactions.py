from sqlalchemy.ext.asyncio import AsyncSession

from contracts.infrastructure import TransactionContextContract
from infrastructure.tx.context import SqlAlchemyTransactionContext
from infrastructure.tx.manager import TransactionManager


def create_transaction_context(
    session_factory: AsyncSession,
) -> SqlAlchemyTransactionContext:
    return SqlAlchemyTransactionContext(session=session_factory)


def create_transaction_manager(
    context: TransactionContextContract,
) -> TransactionManager:
    return TransactionManager(context=context)
