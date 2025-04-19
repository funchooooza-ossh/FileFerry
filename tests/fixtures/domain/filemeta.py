import pytest
from domain.models.dataclasses import FileMeta
from domain.models.enums import FileStatus


@pytest.fixture(scope="function")
def valid_filemeta() -> FileMeta:
    return FileMeta(
        name="filename",
        content_type="application/pdf",
        size=123,
        id="uuid-id",
        status=None,
        reason=None,
    )


@pytest.fixture(scope="function")
def invalid_content_type_filemeta() -> FileMeta:
    return FileMeta(
        name="filename",
        content_type="application/javascript",
        size=123,
        id="uuid-id",
        status=None,
        reason=None,
    )


@pytest.fixture(scope="function")
def invalid_size_filemeta() -> FileMeta:
    return FileMeta(
        name="filename",
        content_type="application/pdf",
        size=0,
        id="uuid-id",
        status=None,
        reason=None,
    )


@pytest.fixture(scope="function")
def failed_filemeta() -> FileMeta:
    return FileMeta(
        name="filename",
        content_type="application/pdf",
        size=0,
        id="uuid-id",
        status=FileStatus.FAILED,
        reason=None,
    )
