import pytest
from domain.models.create_filemeta import create_filemeta
from shared.exceptions.application import InvalidFileParameters


@pytest.mark.unit
def test_create_filemeta_with_valid_data(
    valid_uuid: str, valid_filename: str, valid_filesize: int, valid_ctype: str
):
    meta = create_filemeta(valid_uuid, valid_filename, valid_filesize, valid_ctype)

    assert meta.get_id() == valid_uuid
    assert meta.get_name() == valid_filename
    assert meta.get_size() == valid_filesize
    assert meta.get_content_type() == valid_ctype


@pytest.mark.unit
def test_create_filemeta_with_auto_id(
    valid_filename: str, valid_filesize: int, valid_ctype: str
):
    meta = create_filemeta(None, valid_filename, valid_filesize, valid_ctype)

    assert meta.get_id()  # просто проверяем, что он сгенерирован
    assert meta.get_name() == valid_filename


@pytest.mark.unit
@pytest.mark.parametrize("bad_name", ["", "   "])
def test_create_filemeta_with_empty_filename(
    bad_name: str, valid_uuid: str, valid_filesize: int, valid_ctype: str
):
    with pytest.raises(InvalidFileParameters):
        create_filemeta(valid_uuid, bad_name, valid_filesize, valid_ctype)


@pytest.mark.unit
def test_create_filemeta_with_too_long_filename(
    valid_uuid: str, too_long_filename: str, valid_filesize: int, valid_ctype: str
):
    with pytest.raises(InvalidFileParameters):
        create_filemeta(valid_uuid, too_long_filename, valid_filesize, valid_ctype)


@pytest.mark.unit
def test_create_filemeta_with_slash_in_filename(
    valid_uuid: str,
    illegal_slash_in_filename: str,
    valid_filesize: int,
    valid_ctype: str,
):
    with pytest.raises(InvalidFileParameters):
        create_filemeta(
            valid_uuid, illegal_slash_in_filename, valid_filesize, valid_ctype
        )


@pytest.mark.unit
def test_create_filemeta_with_backslash_in_filename(
    valid_uuid: str,
    illegal_double_backslash_in_filename: str,
    valid_filesize: int,
    valid_ctype: str,
):
    with pytest.raises(InvalidFileParameters):
        create_filemeta(
            valid_uuid,
            illegal_double_backslash_in_filename,
            valid_filesize,
            valid_ctype,
        )


@pytest.mark.unit
@pytest.mark.parametrize("bad_ctype", ["application", "/pdf", "application/"])
def test_create_filemeta_with_invalid_content_type(
    valid_uuid: str, valid_filename: str, valid_filesize: int, bad_ctype: str
):
    with pytest.raises(InvalidFileParameters):
        create_filemeta(valid_uuid, valid_filename, valid_filesize, bad_ctype)


@pytest.mark.unit
@pytest.mark.parametrize("bad_size", [0, -1])
def test_create_filemeta_with_invalid_filesize(
    valid_uuid: str, valid_filename: str, bad_size: int, valid_ctype: str
):
    with pytest.raises(InvalidFileParameters):
        create_filemeta(valid_uuid, valid_filename, bad_size, valid_ctype)


@pytest.mark.unit
def test_create_filemeta_with_invalid_uuid(
    invalid_uuid: str, valid_filename: str, valid_filesize: int, valid_ctype: str
):
    with pytest.raises(InvalidFileParameters):
        create_filemeta(invalid_uuid, valid_filename, valid_filesize, valid_ctype)
