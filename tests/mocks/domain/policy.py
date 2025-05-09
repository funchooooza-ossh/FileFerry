from unittest.mock import MagicMock

import pytest
from contracts.domain import PolicyContract
from shared.exceptions.domain import FilePolicyViolationError


@pytest.fixture(scope="function")
def filepolicy_mock_true() -> PolicyContract:
    policy = MagicMock()
    policy.is_allowed.return_value = True
    return policy


@pytest.fixture(scope="function")
def filepolicy_mock_raises_error() -> PolicyContract:
    policy = MagicMock()
    policy.side_effect = FilePolicyViolationError("Невалидный файл")
    return policy
