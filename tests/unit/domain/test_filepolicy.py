import pytest
from domain.models import FileMeta
from domain.services.upload_policy import FilePolicyDefault
from shared.exceptions.domain import FilePolicyViolationError


@pytest.mark.unit
def test_filepolicy_ok(filemeta: FileMeta):
    meta = filemeta

    result = FilePolicyDefault.is_allowed(meta)

    assert result is True


@pytest.mark.unit
def test_filepolicy_raises_error(disallowed_ctype_filemeta: FileMeta):
    meta = disallowed_ctype_filemeta

    with pytest.raises(FilePolicyViolationError, match="Невалидный файл"):
        result = FilePolicyDefault.is_allowed(meta)

        assert not result
