import pytest
from domain.models import ContentType, FileId, FileMeta, FileName, FileSize
from domain.models.create_filemeta import create_filemeta
from domain.models.value_objects import DomainValueObject


@pytest.mark.unit
def test_filemeta_init(
    ctype: ContentType, filesize: FileSize, filename: FileName, fileid: FileId
):
    meta = FileMeta(fileid, filename, ctype, filesize)

    assert meta is not None
    assert meta.get_id() == fileid.value
    assert meta.get_name() == filename.value
    assert meta.get_content_type() == ctype.value
    assert meta.get_size() == filesize.value

    assert all(
        isinstance(obj, DomainValueObject)
        for obj in [ctype, filesize, filename, fileid]
    )
    assert all(
        isinstance(obj, (FileId, FileName, ContentType, FileSize))
        for obj in [meta._id, meta._name, meta._content_type, meta._size]  # type: ignore violation on scored attr
    )

    assert all(
        not isinstance(obj, DomainValueObject)
        for obj in [
            meta.get_content_type(),
            meta.get_size(),
            meta.get_name(),
            meta.get_id(),
        ]
    )  # check that getter methods returns primitives(str, int, etc..)


@pytest.mark.unit
def test_filemeta_from_raw(
    valid_ctype: str, valid_filename: str, valid_filesize: int, valid_uuid: str
):
    meta = FileMeta.from_raw(
        id=valid_uuid,
        size=valid_filesize,
        content_type=valid_ctype,
        name=valid_filename,
    )

    assert meta is not None
    assert all(
        isinstance(obj, (FileId, FileName, ContentType, FileSize))
        for obj in [meta._id, meta._name, meta._content_type, meta._size]  # type: ignore violation on scored attr
    )


@pytest.mark.unit
def test_filemeta_factory(
    valid_ctype: str, valid_filename: str, valid_filesize: int, valid_uuid: str
):
    meta = create_filemeta(
        file_id=valid_uuid,
        name=valid_filename,
        size=valid_filesize,
        content_type=valid_ctype,
    )

    assert meta is not None
    assert meta.get_id() == valid_uuid
    assert meta.get_content_type() == valid_ctype
    assert meta.get_name() == valid_filename
    assert meta.get_id() == valid_uuid
    assert meta.get_size() == valid_filesize

    assert all(
        isinstance(obj, (FileId, FileName, ContentType, FileSize))
        for obj in [meta._id, meta._name, meta._content_type, meta._size]  # type: ignore violation on scored attr
    )


"""
Writing tests for ValueError on incorrect data is pointless
since these tests are already covered in the tests for value objects,
and both the filemeta factory and FileMeta.from_raw() use these value objects.
"""
