from contracts.infrastructure import (
    CacheInvalidatorContract,
    FileMetaCacheStorageContract,
    FileMetaDataAccessContract,
    FireAndForgetTasksContract,
    TransactionContext,
)
from infrastructure.data_access.alchemy import SQLAlchemyFileMetaDataAccess
from infrastructure.data_access.redis import CachedFileMetaDataAccess


def cache_aside_factory(
    scheduler: FireAndForgetTasksContract,
    redis_storage: FileMetaCacheStorageContract,
    invalidator: CacheInvalidatorContract,
    sql_data_access: FileMetaDataAccessContract,
    ttl: int = 300,
) -> CachedFileMetaDataAccess:
    return CachedFileMetaDataAccess(
        scheduler=scheduler,
        delegate=sql_data_access,
        storage=redis_storage,
        invalidator=invalidator,
        ttl=ttl,
    )


def sql_filemeta_data_access_factory(
    context: TransactionContext,
) -> SQLAlchemyFileMetaDataAccess:
    return SQLAlchemyFileMetaDataAccess(context)


def resolve_data_access(
    with_cache: bool,
    scheduler: FireAndForgetTasksContract | None,
    redis_storage: FileMetaCacheStorageContract | None,
    invalidator: CacheInvalidatorContract | None,
    sql_data_access: SQLAlchemyFileMetaDataAccess,
    ttl: int = 300,
) -> CachedFileMetaDataAccess | SQLAlchemyFileMetaDataAccess:
    if not invalidator or not redis_storage or not with_cache or not scheduler:
        return sql_data_access
    return cache_aside_factory(
        scheduler=scheduler,
        sql_data_access=sql_data_access,
        redis_storage=redis_storage,
        invalidator=invalidator,
        ttl=ttl,
    )
