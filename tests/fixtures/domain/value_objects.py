import pytest
from domain.models import ContentType, FileId, FileName, FileSize


@pytest.fixture(scope="function")
def fileid() -> FileId:
    return FileId.new()


@pytest.fixture(scope="function")
def filesize() -> FileSize:
    return FileSize(123)


@pytest.fixture(scope="function")
def ctype() -> ContentType:
    return ContentType("application/pdf")


@pytest.fixture(scope="function")
def filename() -> FileName:
    return FileName("Filename")
