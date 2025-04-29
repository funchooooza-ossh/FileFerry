from domain.models.dataclasses import FileMeta
from domain.models.value_objects import ContentType, FileId, FileName, FileSize
from infrastructure.models.sqlalchemy.base import Base
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column


class File(Base):
    __tablename__ = "files"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)

    def to_domain(self) -> FileMeta:
        return FileMeta(
            FileId(self.id),
            FileName(self.name),
            ContentType(self.mime_type),
            FileSize(self.size),
        )

    @classmethod
    def from_domain(cls, file_meta: FileMeta) -> "File":
        return cls(
            id=file_meta.get_id(),
            name=file_meta.get_name(),
            mime_type=file_meta.get_content_type(),
            size=file_meta.get_size(),
        )
