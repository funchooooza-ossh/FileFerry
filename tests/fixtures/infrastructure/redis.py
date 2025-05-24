import json

import pytest
from domain.models import FileMeta
from shared.object_mapping.filemeta import FileMetaMapper


@pytest.fixture(scope="function")
def filemeta_bytes(filemeta: FileMeta) -> bytes:
    return json.dumps(FileMetaMapper.serialize_filemeta(filemeta)).encode("utf-8")


@pytest.fixture(scope="function")
def filemeta_string(filemeta: FileMeta) -> str:
    return json.dumps(FileMetaMapper.serialize_filemeta(filemeta))


@pytest.fixture(scope="function")
def cache_prefix() -> str:
    return "file:meta"
