from loguru import logger
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from contracts.infrastructure import SQLAlchemyDataAccessContract, TransactionContext
from domain.models import FileMeta
from infrastructure.models.sqlalchemy.file import File
from shared.exceptions.handlers.alchemy_handler import wrap_sqlalchemy_failure


class SQLAlchemyDataAccess(SQLAlchemyDataAccessContract):
    def __init__(self, context: TransactionContext) -> None:
        self._context = context

    @property
    def session(self) -> AsyncSession:
        return self._context.session

    @wrap_sqlalchemy_failure
    async def save(self, file_meta: FileMeta) -> FileMeta:
        model = File.from_domain(file_meta)
        self.session.add(model)
        await self.session.flush()
        return file_meta

    @wrap_sqlalchemy_failure
    async def get(self, file_id: str) -> FileMeta:
        query = await self.session.execute(select(File).where(File.id == file_id))
        model = query.scalar_one()
        return model.to_domain()

    @wrap_sqlalchemy_failure
    async def delete(self, file_id: str) -> None:
        query = await self.session.execute(select(File).where(File.id == file_id))
        model = query.scalar_one()
        await self.session.delete(model)
        await self.session.flush()
        return

    @wrap_sqlalchemy_failure
    async def update(self, meta: FileMeta) -> FileMeta:
        query = await self.session.execute(select(File).where(File.id == meta.get_id()))
        model = query.scalar_one()

        model.name = meta.get_name()
        model.size = meta.get_size()
        model.mime_type = meta.get_content_type()

        await self.session.flush()

        return model.to_domain()

    async def healtcheck(self) -> bool:
        try:
            query = await self.session.execute(text("SELECT 1"))
            query.scalar_one()
            return True
        except Exception as exc:
            logger.critical(f"[DATABASE] Db healtcheck failed: {exc}")
            return False
