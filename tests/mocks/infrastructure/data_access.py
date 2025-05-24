from unittest.mock import AsyncMock

import pytest
from infrastructure.data_access.alchemy import SQLAlchemyFileMetaDataAccess
from infrastructure.data_access.redis import CachedFileMetaDataAccess
from infrastructure.storage.redis import RedisFileMetaCacheStorage
from infrastructure.tasks.consistence import CacheInvalidator
from infrastructure.tasks.scheduler import AsyncioFireAndForget
from infrastructure.tx.context import SqlAlchemyTransactionContext


@pytest.fixture(scope="function")
def mock_sql_data_access() -> SQLAlchemyFileMetaDataAccess:
    dao = AsyncMock()
    return dao


@pytest.fixture(scope="function")
def mock_cached_data_access() -> CachedFileMetaDataAccess:
    cached_dao = AsyncMock()
    return cached_dao


@pytest.fixture(scope="function")
def sql_dao(tx_context: SqlAlchemyTransactionContext) -> SQLAlchemyFileMetaDataAccess:
    dao = SQLAlchemyFileMetaDataAccess(context=tx_context)
    dao.get = AsyncMock()
    dao.delete = AsyncMock()
    dao.save = AsyncMock()
    dao.update = AsyncMock()
    dao.healthcheck = AsyncMock()
    return dao


@pytest.fixture(scope="function")
def cached_dao(
    sql_dao: SQLAlchemyFileMetaDataAccess,
    mock_cache_invalidator: CacheInvalidator,
    mock_redis_storage: RedisFileMetaCacheStorage,
) -> CachedFileMetaDataAccess:
    scheduler = AsyncioFireAndForget()
    dao = CachedFileMetaDataAccess(
        delegate=sql_dao,
        invalidator=mock_cache_invalidator,
        scheduler=scheduler,
        storage=mock_redis_storage,
    )
    dao.delete = AsyncMock()
    dao.get = AsyncMock()
    dao.save = AsyncMock()
    dao.update = AsyncMock()
    dao.healthcheck = AsyncMock()
    return dao
