from domain.models.dataclasses import FileMeta
from infrastructure.models.sqlalchemy.base import Base
from infrastructure.types.filemeta import ORMFileMeta
from shared.object_mapping.filemeta import FileMetaMapper
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column


class File(Base):
    """
    ORM репрезентация бизнес модели FileMeta для SQLAlchemy
    """

    __tablename__ = "files"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)

    def to_domain(self) -> FileMeta:
        return FileMetaMapper.filemeta_from_orm(
            ORMFileMeta(
                id=self.id, name=self.name, size=self.size, mime_type=self.mime_type
            )
        )

    @classmethod
    def from_domain(cls, file_meta: FileMeta) -> "File":
        return cls(**FileMetaMapper.filemeta_to_orm(file_meta))
