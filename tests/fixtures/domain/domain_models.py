import pytest
from domain.models import ContentType, FileId, FileMeta, FileName, FileSize


@pytest.fixture(scope="function")
def filemeta(
    fileid: FileId, filename: FileName, filesize: FileSize, ctype: ContentType
) -> FileMeta:
    return FileMeta(fileid, filename, ctype, filesize)


@pytest.fixture(scope="function")
def disallowed_ctype_filemeta(
    fileid: FileId, filename: FileName, filesize: FileSize
) -> FileMeta:
    ctype = ContentType("application/x-empty")
    return FileMeta(fileid, filename, ctype, filesize)
