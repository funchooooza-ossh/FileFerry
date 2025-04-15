from sqlalchemy.ext.asyncio import AsyncSession
from repositories.sqlalchemy.base import BaseSqlAlchemyRepository
from models import File
from utils.registry import Registrator, DBType, RepositoryName


class FileRepository(BaseSqlAlchemyRepository[File]):
    model = File

    def __init__(self, session: AsyncSession):
        super().__init__(session)


Registrator.register(
    db_type=DBType.SQLALCHEMY, name=RepositoryName.FILE, repo_class=FileRepository
)
