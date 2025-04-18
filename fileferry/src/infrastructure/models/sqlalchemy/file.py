from domain.models.dataclasses import FileMeta
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
            id=self.id, name=self.name, content_type=self.mime_type, size=self.size
        )

    @classmethod
    def from_domain(cls, file_meta: FileMeta) -> "File":
        return cls(
            id=file_meta.id,
            name=file_meta.name,
            mime_type=file_meta.content_type,
            size=file_meta.size,
        )
