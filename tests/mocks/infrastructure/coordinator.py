from unittest.mock import AsyncMock

import pytest
from infrastructure.coordination.minio_sqla import SqlAlchemyMinioCoordinator


@pytest.fixture(scope="function")
def mock_coordinator() -> SqlAlchemyMinioCoordinator:
    coordinator = AsyncMock()
    coordinator.storage = AsyncMock()
    coordinator.data_access = AsyncMock()
    coordinator._transaction = AsyncMock()

    coordinator.__aenter__ = AsyncMock(return_value=coordinator)
    coordinator.__aexit__ = AsyncMock()
    coordinator.commit = AsyncMock()
    coordinator.rollback = AsyncMock()

    return coordinator
