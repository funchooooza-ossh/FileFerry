import pytest
from infrastructure.models.sqlalchemy.file import File


@pytest.fixture(scope="function")
def valid_file() -> File:
    return File(id="uuid-id", name="filename", mime_type="application/pdf", size=123)
