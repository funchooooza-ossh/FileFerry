import random
import uuid

import pytest
from domain.models.value_objects import FileId, FileName


@pytest.mark.asyncio
async def test_file_id_generation():
    file_id = FileId.new()

    assert uuid.UUID(file_id.value)


@pytest.mark.asyncio
async def test_file_id_initialize():
    file_id = uuid.uuid4().hex

    file_id_vo = FileId(value=file_id)

    assert file_id_vo is not None
    assert file_id_vo.value == file_id


@pytest.mark.asyncio
async def test_file_id_initialize_not_valid_uuid():
    file_id = "something"

    with pytest.raises(ValueError, match="Invalid UUID"):
        file_id_vo = FileId(value=file_id)

        assert (
            file_id_vo is not None
        )  # инициализировался, но выбросил ошибку на пост ините


@pytest.mark.asyncio
async def test_filename_initialize():
    string_name = "something_that_is_ok"

    file_name = FileName(value=string_name)

    assert file_name is not None
    assert file_name.value == string_name


@pytest.mark.asyncio
async def test_filename_illegal_chars():
    string_name = "name\\name"

    with pytest.raises(ValueError, match="File name contains illegal characters"):
        filename = FileName(value=string_name)

        assert filename is not None


@pytest.mark.asyncio
async def test_filename_too_long():
    chars = ["a", "b", "c", "d", "e"]
    string_name = "".join(random.choice(chars) for _ in range(256))

    with pytest.raises(ValueError, match="File name too long"):
        filename = FileName(value=string_name)

        assert filename is not None


@pytest.mark.asyncio
async def test_filename_empty():
    string_name = ""

    with pytest.raises(ValueError, match="File name cannot be empty"):
        filename = FileName(value=string_name)

        assert filename is not None
