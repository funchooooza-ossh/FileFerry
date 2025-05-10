import pytest
from domain.models import FileMeta
from infrastructure.data_access.alchemy import SQLAlchemyFileMetaDataAccess
from infrastructure.tx.context import SqlAlchemyTransactionContext
from shared.exceptions.infrastructure import NoResultFoundError


@pytest.mark.unit
async def test_sql_data_access_save_get(
    tx_context: SqlAlchemyTransactionContext, filemeta: FileMeta
):
    dao = SQLAlchemyFileMetaDataAccess(context=tx_context)

    await tx_context.begin()

    await dao.save(filemeta)

    meta = await dao.get(filemeta.get_id())

    assert meta.get_id() == filemeta.get_id()
    assert meta.get_size() == filemeta.get_size()
    assert meta.get_content_type() == filemeta.get_content_type()
    assert meta.get_name() == filemeta.get_name()

    await tx_context.close()


@pytest.mark.unit
async def test_sql_data_access_save_delete(
    tx_context: SqlAlchemyTransactionContext, filemeta: FileMeta
):
    dao = SQLAlchemyFileMetaDataAccess(context=tx_context)

    await tx_context.begin()

    await dao.save(filemeta)

    meta = await dao.get(filemeta.get_id())

    await dao.delete(meta.get_id())

    with pytest.raises(NoResultFoundError):
        new_meta = await dao.get(meta.get_id())

        assert meta
        assert not new_meta
