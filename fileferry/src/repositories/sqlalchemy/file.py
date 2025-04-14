from repositories.sqlalchemy.base import BaseSqlAlchemyRepository
from models import File


class FileRepository(BaseSqlAlchemyRepository[File]):
    model = File
