import pytest
from domain.models.dataclasses import FileMeta
from composition.meta_factory import create_filemeta


@pytest.fixture(scope="function")
def valid_filemeta() -> FileMeta:
    return create_filemeta(
        name="filename",
        content_type="application/pdf",
        size=123,
    )


@pytest.fixture(scope="function")
def invalid_content_type_filemeta() -> FileMeta:
    return create_filemeta(
        name="filename",
        content_type="application/javascript",
        size=123,
    )


@pytest.fixture(scope="function")
def failed_filemeta() -> FileMeta:
    return create_filemeta(
        name="filename",
        content_type="application/pdf",
        size=0,
    )
