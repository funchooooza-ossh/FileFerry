from sqlalchemy.ext.asyncio import AsyncSession
from repositories.sqlalchemy.base import BaseSqlAlchemyRepository
from models import File
from utils.registry import SqlAlchemyRegistry


@SqlAlchemyRegistry.register(name="file")
class FileRepository(BaseSqlAlchemyRepository[File]):
    model = File

    def __init__(self, session: AsyncSession):
        super().__init__(session)
