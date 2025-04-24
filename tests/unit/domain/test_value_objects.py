import pytest
import uuid
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
