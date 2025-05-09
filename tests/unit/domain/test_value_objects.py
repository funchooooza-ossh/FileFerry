import uuid

import pytest
from domain.models import ContentType, FileId, FileName, FileSize


@pytest.mark.unit
def test_fileid_creation(valid_uuid: str):
    value = valid_uuid

    vo = FileId(value)

    assert vo is not None
    assert vo.value == value


@pytest.mark.unit
def test_fileid_raises_value_error_on_invalid_uuid(invalid_uuid: str):
    value = invalid_uuid

    with pytest.raises(ValueError, match="Invalid UUID"):
        vo = FileId(value)

        assert vo is not None


@pytest.mark.unit
def test_fileid_raises_value_error_on_empty_value(empty_value: None):
    value = empty_value

    with pytest.raises(ValueError, match="Invalid UUID"):
        vo = FileId(value)  # type: ignore

        assert vo is not None


@pytest.mark.unit
def test_fileid_generation():
    vo = FileId.new()

    assert uuid.UUID(vo.value)


@pytest.mark.unit
def test_filename_creation(valid_filename: str):
    value = valid_filename

    vo = FileName(value)

    assert vo is not None
    assert vo.value == value


@pytest.mark.unit
def test_filename_value_error_on_too_long_value(too_long_filename: str):
    value = too_long_filename
    with pytest.raises(ValueError, match="File name too long"):
        vo = FileName(value)

        assert vo is not None


@pytest.mark.unit
def test_filename_value_error_on_slash(illegal_slash_in_filename: str):
    value = illegal_slash_in_filename

    with pytest.raises(ValueError, match="File name contains illegal characters"):
        vo = FileName(value)

        assert vo is not None


@pytest.mark.unit
def test_filename_value_error_on_double_backslash(
    illegal_double_backslash_in_filename: str,
):
    value = illegal_double_backslash_in_filename

    with pytest.raises(ValueError, match="File name contains illegal characters"):
        vo = FileName(value)

        assert vo is not None


@pytest.mark.unit
def test_filename_raises_value_error_on_empty_value(empty_value: None):
    value = empty_value

    with pytest.raises(ValueError, match="TypeError or empty string detected."):
        vo = FileName(value)  # type: ignore type annotation != stronly typed. we can init this with Any

        assert vo is not None


@pytest.mark.unit
def test_filename_raises_value_error_on_empty_string():
    value = ""

    with pytest.raises(ValueError, match="TypeError or empty string detected"):
        vo = FileName(value)

        assert vo is not None


@pytest.mark.unit
def test_ctype_creation(valid_ctype: str):
    value = valid_ctype

    vo = ContentType(value)

    assert vo is not None
    assert vo.value == value


@pytest.mark.unit
def test_ctype_raises_value_error_on_none(empty_value: None):
    value = empty_value

    with pytest.raises(ValueError, match="Invalid MIME type format"):
        vo = ContentType(value)  # type: ignore

        assert vo is not None


@pytest.mark.unit
def test_ctype_raises_value_error_on_empty_string():
    value = ""

    with pytest.raises(ValueError, match="Invalid MIME type format"):
        vo = ContentType(value)

        assert vo is not None


@pytest.mark.unit
def test_ctype_raises_value_error_on_misstype():
    value = int(1)

    with pytest.raises(ValueError, match="Invalid MIME type format"):
        vo = ContentType(value)  # type: ignore

        assert vo is not None


@pytest.mark.unit
def test_ctype_raises_value_error_on_incomplete_ctype_main_part(
    incomplete_ctype_main: str,
):
    value = incomplete_ctype_main

    with pytest.raises(ValueError, match="Incomplete MIME type"):
        vo = ContentType(value)

        assert vo is not None


@pytest.mark.unit
def test_ctype_raises_value_error_on_incomplete_ctype_sub_part(
    incomplete_ctype_sub: str,
):
    value = incomplete_ctype_sub

    with pytest.raises(ValueError, match="Incomplete MIME type"):
        vo = ContentType(value)

        assert vo is not None


@pytest.mark.unit
def test_filesize_creation(valid_filesize: int):
    value = valid_filesize

    vo = FileSize(value)

    assert vo is not None
    assert vo.value == value


@pytest.mark.unit
def test_filesize_raises_value_error_on_miss_type(empty_value: None):
    value = empty_value

    with pytest.raises(ValueError, match="File size must be an integer"):
        vo = FileSize(value)  # type: ignore

        assert vo is not None


@pytest.mark.unit
def test_filesize_raises_value_error_on_zero_value(filesize_zero_value: int):
    value = filesize_zero_value

    with pytest.raises(ValueError, match="File size must be positive"):
        vo = FileSize(value)

        assert vo is not None


@pytest.mark.unit
def test_filesize_raises_value_error_on_negative_value(negative_filesize: int):
    value = negative_filesize

    with pytest.raises(ValueError, match="File size must be positive"):
        vo = FileSize(value)

        assert vo is not None
