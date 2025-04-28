from typing import Optional

from loguru import logger
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from contracts.infrastructure import SQLAlchemyDataAccessContract
from domain.models import FileMeta
from infrastructure.models.sqlalchemy.file import File
from shared.exceptions.exc_classes.infrastructure import RepositoryRunTimeError
from shared.exceptions.handlers.alchemy_handler import wrap_sqlalchemy_failure


class SQLAlchemyDataAccess(SQLAlchemyDataAccessContract):
    def __init__(self, session: Optional[AsyncSession] = None) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        if not self._session:
            raise RepositoryRunTimeError(
                "[CRITICAL] -- You can not use data access with no session context"
            )
        return self._session

    def bind_session(self, session: AsyncSession) -> None:
        """Явно привязывает сессию к DataAccess перед началом работы."""
        if self._session is not None:
            raise RepositoryRunTimeError("[CRITICAL] DataAccess session already bound")
        self._session = session

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
    async def update(self, meta: FileMeta) -> Optional[FileMeta]:
        query = await self.session.execute(select(File).where(File.id == meta.id.value))
        model = query.scalar_one()

        model.name = meta.name.value
        model.size = meta.size.value
        model.content_type = meta.content_type.value

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
