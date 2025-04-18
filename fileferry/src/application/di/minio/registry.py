from typing import Literal

from pydantic_settings import BaseSettings

from shared.types.minio_creds import MinioCreds


class MinioCredentials(BaseSettings):
    access: str
    secret: str
    endpoint: str
    secure: bool

    def to_typed_dict(self) -> MinioCreds:
        return MinioCreds(
            access=self.access,
            secret=self.secret,
            endpoint=self.endpoint,
            secure=self.secure,
        )


class MinioDefaultCredentials(MinioCredentials):
    class Config:
        env_file = "minio.env"
        env_file_encoding = "utf-8"
        case_sensitive = False


minio_default = MinioDefaultCredentials()


KnownMinioClients = Literal["default", "archive", "private"]

minio_clients: dict[KnownMinioClients, MinioCreds] = {
    "default": minio_default.to_typed_dict()
}
