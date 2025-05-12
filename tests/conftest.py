pytest_plugins = [
    "fixtures.base",
    "fixtures.domain.value_objects",
    "fixtures.domain.domain_models",
    "fixtures.infrastructure.sqlalchemy",
    "mocks.infrastructure.coordinator",
    "mocks.infrastructure.sqlalchemy",
    "mocks.infrastructure.tx.context",
    "mocks.infrastructure.data_access",
    "mocks.infrastructure.filehelper",
    "mocks.infrastructure.minio_client",
    "mocks.domain.meta_factory",
    "mocks.domain.policy",
]
