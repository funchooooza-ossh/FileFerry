from models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger


class File(Base):
    __tablename__ = "files"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    size: Mapped[int] = mapped_column(BigInteger, nullable=False)

    def __init__(self, name: str, slug: str, mime_type: str, size: int) -> None:
        self.name = name
        self.slug = slug
        self.mime_type = mime_type
        self.size = size

    def __repr__(self):
        return f"<File {self.slug} {self.mime_type} {self.size}>"
