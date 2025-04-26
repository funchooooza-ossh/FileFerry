from enum import StrEnum

from pydantic_settings import BaseSettings

from shared.types.minio_creds import MinioCreds


class MinioCredentials(BaseSettings):
    access: str
    secret: str
    endpoint: str
    secure: bool

    def to_typed_dict(self) -> MinioCreds:
        return {
            "access": self.access,
            "secret": self.secret,
            "endpoint": self.endpoint,
            "secure": self.secure,
        }

    def __repr__(self) -> str:
        return "<MiniOCredentials [secure]>"


class MinioDefaultCredentials(MinioCredentials):
    class Config:
        env_file = "minio.env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class ExistingBuckets(StrEnum):
    DEFAULT = "default-bucket"

    @property
    def description(self) -> str:
        match self:
            case ExistingBuckets.DEFAULT:
                return "Dev bucket.Shouldn't really exists in production."
