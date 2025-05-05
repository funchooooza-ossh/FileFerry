from contracts.infrastructure import (
    FileMetaDataAccessContract,
    StorageAccessContract,
    TransactionManagerContract,
)
from infrastructure.coordination.minio_sqla import SqlAlchemyMinioCoordinator


def sql_minio_coordinator_factory(
    transaction: TransactionManagerContract,
    storage: StorageAccessContract,
    data_access: FileMetaDataAccessContract,
) -> SqlAlchemyMinioCoordinator:
    return SqlAlchemyMinioCoordinator(
        transaction=transaction, storage=storage, data_access=data_access
    )
