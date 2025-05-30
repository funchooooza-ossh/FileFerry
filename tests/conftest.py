import logging

from loguru import logger

pytest_plugins = [
    "fixtures.base",
    "fixtures.domain.value_objects",
    "fixtures.domain.domain_models",
    "fixtures.infrastructure.sqlalchemy",
    "fixtures.infrastructure.redis",
    "fixtures.infrastructure.tasks",
    "mocks.infrastructure.coordinator",
    "mocks.infrastructure.sqlalchemy",
    "mocks.infrastructure.tx.context",
    "mocks.infrastructure.tx.manager",
    "mocks.infrastructure.data_access",
    "mocks.infrastructure.filehelper",
    "mocks.infrastructure.coordinator",
    "mocks.infrastructure.minio.client",
    "mocks.infrastructure.minio.storage",
    "mocks.infrastructure.redis.client",
    "mocks.infrastructure.redis.storage",
    "mocks.infrastructure.tasks.manager",
    "mocks.infrastructure.tasks.consistence",
    "mocks.domain.meta_factory",
    "mocks.domain.policy",
]


class PropagateHandler(logging.Handler):
    def emit(self, record):  # type: ignore
        logging.getLogger(record.name).handle(record)


logger.remove()
logger.add(PropagateHandler(), level="TRACE")
