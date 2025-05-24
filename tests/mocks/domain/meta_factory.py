from collections.abc import Callable
from typing import Optional
from unittest.mock import MagicMock

import pytest
from domain.models import FileMeta
from shared.exceptions.application import InvalidFileParameters


@pytest.fixture(scope="function")
def meta_factory_mock(
    filemeta: FileMeta,
) -> Callable[[Optional[str], str, int, str], FileMeta]:
    factory = MagicMock()
    factory.return_value = filemeta
    return factory


@pytest.fixture(scope="function")
def meta_factory_mock_raises_error() -> (
    Callable[[Optional[str], str, int, str], FileMeta]
):
    factory = MagicMock()
    factory.side_effect = InvalidFileParameters("Unprocessable entity")
    return factory
