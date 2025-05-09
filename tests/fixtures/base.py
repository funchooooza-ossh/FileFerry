import random
import string
import uuid

import pytest


@pytest.fixture(scope="function")
def valid_uuid() -> str:
    return uuid.uuid4().hex


@pytest.fixture(scope="function")
def invalid_uuid() -> str:
    return uuid.uuid4().hex[:8]


@pytest.fixture(scope="function")
def valid_filename() -> str:
    return "Filename"


@pytest.fixture(scope="function")
def too_long_filename() -> str:
    return "".join(random.choice(string.ascii_lowercase) for _ in range(256))


@pytest.fixture(scope="function")
def illegal_slash_in_filename() -> str:
    return "str/str"


@pytest.fixture(scope="function")
def illegal_double_backslash_in_filename() -> str:
    return "str\\str"


@pytest.fixture(scope="function")
def valid_ctype() -> str:
    return "appliaction/pdf"


@pytest.fixture(scope="function")
def invalid_ctype() -> str:
    return "application"


@pytest.fixture(scope="function")
def incomplete_ctype_main() -> str:
    return "/pdf"


@pytest.fixture(scope="function")
def incomplete_ctype_sub() -> str:
    return "application/"


@pytest.fixture(scope="function")
def valid_filesize() -> int:
    return 123


@pytest.fixture(scope="function")
def filesize_zero_value() -> int:
    return 0


@pytest.fixture(scope="function")
def negative_filesize() -> int:
    return -1


@pytest.fixture(scope="function")
def empty_value() -> None:
    return None
