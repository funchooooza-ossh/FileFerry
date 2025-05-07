import time

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from contracts.infrastructure import FileMetaDataAccessContract, TransactionContext
from domain.models import FileMeta
from infrastructure.exceptions.handlers.alchemy_handler import wrap_sqlalchemy_failure
from infrastructure.models.sqlalchemy.file import File
from infrastructure.types.health import ComponentState, ComponentStatus


class SQLAlchemyFileMetaDataAccess(FileMetaDataAccessContract):
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

    async def healthcheck(self) -> ComponentStatus:
        start = time.perf_counter()
        try:
            await self.session.execute(text("SELECT 1"))
            latency = (time.perf_counter() - start) * 1000  # мс

            version_result = await self.session.execute(text("SELECT version()"))
            version_row = version_result.fetchone()
            version = version_row[0] if version_row else "unknown"

            status: ComponentState = "ok" if latency <= 100.0 else "degraded"

            return ComponentStatus(
                status=status, latency_ms=latency, details={"version": version}
            )

        except Exception as exc:
            return ComponentStatus(status="down", error=str(exc))
